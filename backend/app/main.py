import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import auth, analysis, projects, synthesis, advanced
from app.core.database import init_db

AVATARS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "avatars")
os.makedirs(AVATARS_DIR, exist_ok=True)

app = FastAPI(title="SciSynthesis — AI Research Platform")

# CORS — restrict to frontend origin only
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Security headers middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)

@app.on_event("startup")
async def on_startup():
    await init_db()

# Include Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(advanced.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(synthesis.router, prefix="/api/v1")
app.mount("/avatars", StaticFiles(directory=AVATARS_DIR), name="avatars")



@app.get("/api/v1/health")
def health_check():
    return {"status": "active", "system": "enterprise"}
