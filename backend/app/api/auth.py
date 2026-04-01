import os
import uuid
import secrets
import hmac
from datetime import timedelta, datetime, timezone
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.core import security
from app.core.database import get_db
from app.models.user import User as UserModel
from app.models.paper import Paper as PaperModel
from app.models.project import Project as ProjectModel, Note as NoteModel
from app.models.schemas import UserCreate, Token, User as UserSchema, UserUpdate, UserStats
from app.api.deps import get_current_user

# In-memory OTP store: { phone_number: { "otp": "123456", "expiry": datetime, "user_id": int } }
_otp_store: Dict[str, dict] = {}

AVATARS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "avatars")
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/stats", response_model=UserStats)
async def get_stats(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    papers = await db.execute(select(func.count()).where(PaperModel.user_id == current_user.id))
    projects = await db.execute(select(func.count()).where(ProjectModel.user_id == current_user.id))
    notes = await db.execute(select(func.count()).where(NoteModel.user_id == current_user.id))
    return UserStats(
        papers_analyzed=papers.scalar() or 0,
        projects_created=projects.scalar() or 0,
        notes_written=notes.scalar() or 0,
    )

@router.put("/me", response_model=UserSchema)
async def update_me(
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    update_data = user_in.model_dump(exclude_unset=True)

    if "password" in update_data:
        hashed_password = security.get_password_hash(update_data["password"])
        current_user.hashed_password = hashed_password
        del update_data["password"]

    if "email" in update_data and update_data["email"] != current_user.email:
        existing = await db.execute(select(UserModel).where(UserModel.email == update_data["email"]))
        if existing.scalars().first():
            raise HTTPException(status_code=400, detail="This email is already registered to another account.")

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/me/avatar", response_model=UserSchema)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WebP, or GIF images are allowed.")
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File size must be under 5MB.")

    # Delete old avatar if exists
    if current_user.profile_picture:
        old_path = os.path.join(AVATARS_DIR, current_user.profile_picture)
        if os.path.exists(old_path):
            os.remove(old_path)

    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    filename = f"{current_user.id}_{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(AVATARS_DIR, filename)
    os.makedirs(AVATARS_DIR, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(contents)

    current_user.profile_picture = filename
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.delete("/me/avatar", response_model=UserSchema)
async def delete_avatar(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.profile_picture:
        old_path = os.path.join(AVATARS_DIR, current_user.profile_picture)
        if os.path.exists(old_path):
            os.remove(old_path)
        current_user.profile_picture = None
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
    return current_user

class OTPRequest(BaseModel):
    phone_number: str

class OTPVerify(BaseModel):
    phone_number: str
    otp: str

@router.post("/send-otp")
async def send_otp(req: OTPRequest, db: AsyncSession = Depends(get_db)):
    """Generate a 6-digit OTP for the given phone number."""
    result = await db.execute(
        select(UserModel).where(UserModel.phone_number == req.phone_number)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this phone number. Please register first or add your phone number in Profile settings.")

    otp_code = str(secrets.randbelow(900000) + 100000)  # Cryptographically secure OTP
    expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    _otp_store[req.phone_number] = {"otp": otp_code, "expiry": expiry, "user_id": user.id}

    # In production: send via SMS (Twilio/MSG91 etc.)
    # OTP is NOT returned in the response for security
    return {
        "message": f"OTP sent to {req.phone_number}",
        "expires_in": "5 minutes"
    }

@router.post("/verify-otp", response_model=Token)
async def verify_otp(req: OTPVerify, db: AsyncSession = Depends(get_db)):
    """Verify OTP and return JWT access token."""
    record = _otp_store.get(req.phone_number)
    if not record:
        raise HTTPException(status_code=400, detail="No OTP was sent to this number. Please request a new one.")

    if datetime.now(timezone.utc) > record["expiry"]:
        _otp_store.pop(req.phone_number, None)
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    if not hmac.compare_digest(req.otp.strip(), record["otp"]):
        raise HTTPException(status_code=400, detail="Invalid OTP. Please check and try again.")

    # OTP valid — fetch user and issue token
    result = await db.execute(select(UserModel).where(UserModel.id == record["user_id"]))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    _otp_store.pop(req.phone_number, None)  # One-time use
    access_token = security.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserSchema)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.email == user_in.email))
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(user_in.password)
    user_dict = user_in.model_dump()
    del user_dict["password"]

    new_user = UserModel(**user_dict, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.email == form_data.username))
    user = result.scalars().first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
