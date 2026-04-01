from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./research_assistant.db")

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    # Import models here to ensure they are registered with Base.metadata
    from app.models.user import User
    from app.models.paper import Paper
    from app.models.chunk import DocumentChunk
    from app.models.project import Project, Note
    from app.models.search_history import SearchHistory

    from sqlalchemy import text
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Migrate: add new columns to existing tables without breaking if already present
        for sql in [
            "ALTER TABLE users ADD COLUMN created_at DATETIME",
            "ALTER TABLE users ADD COLUMN profile_picture VARCHAR",
        ]:
            try:
                await conn.execute(text(sql))
            except Exception:
                pass  # Column already exists
        # Backfill created_at for existing users
        await conn.execute(text(
            "UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"
        ))

