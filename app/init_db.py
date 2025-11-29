"""
Initialize database - run migrations and optionally seed data.
Usage: python -m app.init_db
"""
from app.database import engine, init_db
from alembic.config import Config
from alembic import command
import os

def run_migrations():
    """Run Alembic migrations to latest version"""
    alembic_cfg = Config(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    print("✅ Database migrations completed")

def initialize():
    """Initialize database - run migrations"""
    print("🚀 Initializing database...")
    run_migrations()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    initialize()

