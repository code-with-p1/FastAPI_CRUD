from fastapi import FastAPI
from app.routes.async_routes import router as async_router
from app.routes.sync_routes import router as sync_router
from app.database.db import init_db

app = FastAPI(title="User CRUD API with SQLite")

# Initialize SQLite database
init_db()

# Mount routes
app.include_router(async_router, prefix="/async", tags=["Async"])
app.include_router(sync_router, prefix="/sync", tags=["Sync"])