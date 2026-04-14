import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import auth, analysis, projects, synthesis, advanced, review
from app.core.database import init_db
from app.core.limiter import limiter

logger = logging.getLogger("scisynthesis")

AVATARS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "avatars")
os.makedirs(AVATARS_DIR, exist_ok=True)

app = FastAPI(title="SciSynthesis — AI Research Platform")

# ── Rate limiter ──────────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS — restrict to known frontend origins only ────────────────────────────
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,                          # required for cookie auth
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


# ── Security headers ──────────────────────────────────────────────────────────
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response

app.add_middleware(SecurityHeadersMiddleware)


@app.on_event("startup")
async def on_startup():
    await init_db()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )
    logger.info("SciSynthesis backend started.")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router,     prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(advanced.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(synthesis.router,prefix="/api/v1")
app.include_router(review.router,   prefix="/api/v1")   # Literature review + gap detection

app.mount("/avatars", StaticFiles(directory=AVATARS_DIR), name="avatars")


@app.get("/api/v1/health")
def health_check():
    return {"status": "active", "system": "enterprise"}
