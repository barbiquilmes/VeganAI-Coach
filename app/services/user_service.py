"""
User service - handles user creation and retrieval.
For MVP, we'll use a simple single-user approach or create users on-demand.
"""
from sqlalchemy.orm import Session
from app.db_models import User
from typing import Optional


def get_or_create_user(db: Session, user_id: Optional[int] = None) -> User:
    """
    Get existing user or create a new one.
    For MVP, we'll use a simple approach: get first user or create one.
    In production, you'd use proper authentication.
    
    Args:
        db: Database session
        user_id: Optional user ID (for future multi-user support)
    
    Returns:
        User object
    """
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
    
    # For MVP: get first user or create one
    user = db.query(User).first()
    if not user:
        user = User(preferences_json={})
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

