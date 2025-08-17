from sqlalchemy import create_engine, Column, Integer, String, UUID as SQLUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import uuid

# SQLite database URLs
SQLITE_URL = "sqlite:///./users.db"
SQLITE_ASYNC_URL = "sqlite+aiosqlite:///./users.db"

# Sync engine and session
sync_engine = create_engine(SQLITE_URL, echo=False)
SyncSessionLocal = sessionmaker(bind=sync_engine)

# Async engine and session
async_engine = create_async_engine(SQLITE_ASYNC_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# SQLAlchemy Base
Base = declarative_base()

# User model for SQLAlchemy
class UserDB(Base):
    __tablename__ = "users"
    id = Column(SQLUUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)

def init_db():
    Base.metadata.create_all(bind=sync_engine)