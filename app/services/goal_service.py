"""
Goal service - handles goal creation, retrieval, and management.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db_models import Goal, User
from app.models import GoalCreate, GoalUpdate
from typing import List, Optional
from fastapi import HTTPException


def create_goal(db: Session, user_id: int, goal_data: GoalCreate) -> Goal:
    """
    Create a new learning goal for a user.
    
    Args:
        db: Database session
        user_id: User ID
        goal_data: Goal creation data
    
    Returns:
        Created Goal object
    
    Raises:
        HTTPException: If user doesn't exist
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create goal
    goal = Goal(
        user_id=user_id,
        title=goal_data.title,
        description=goal_data.description,
        target_recipes_per_week=goal_data.target_recipes_per_week,
        target_skill=goal_data.target_skill,
        status="active"
    )
    
    db.add(goal)
    db.commit()
    db.refresh(goal)
    
    return goal


def get_goal(db: Session, goal_id: int, user_id: Optional[int] = None) -> Optional[Goal]:
    """
    Get a goal by ID, optionally verifying it belongs to a user.
    
    Args:
        db: Database session
        goal_id: Goal ID
        user_id: Optional user ID to verify ownership
    
    Returns:
        Goal object or None
    """
    query = db.query(Goal).filter(Goal.id == goal_id)
    
    if user_id:
        query = query.filter(Goal.user_id == user_id)
    
    return query.first()


def get_user_goals(db: Session, user_id: int, status: Optional[str] = None) -> List[Goal]:
    """
    Get all goals for a user, optionally filtered by status.
    
    Args:
        db: Database session
        user_id: User ID
        status: Optional status filter (active, completed, paused)
    
    Returns:
        List of Goal objects
    """
    query = db.query(Goal).filter(Goal.user_id == user_id)
    
    if status:
        query = query.filter(Goal.status == status)
    
    return query.order_by(desc(Goal.created_at)).all()


def update_goal(db: Session, goal_id: int, user_id: int, goal_data: GoalUpdate) -> Goal:
    """
    Update an existing goal.
    
    Args:
        db: Database session
        goal_id: Goal ID
        user_id: User ID (to verify ownership)
        goal_data: Update data
    
    Returns:
        Updated Goal object
    
    Raises:
        HTTPException: If goal not found or doesn't belong to user
    """
    goal = get_goal(db, goal_id, user_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Update fields if provided
    if goal_data.title is not None:
        goal.title = goal_data.title
    if goal_data.description is not None:
        goal.description = goal_data.description
    if goal_data.target_recipes_per_week is not None:
        goal.target_recipes_per_week = goal_data.target_recipes_per_week
    if goal_data.target_skill is not None:
        goal.target_skill = goal_data.target_skill
    if goal_data.status is not None:
        goal.status = goal_data.status
    
    db.commit()
    db.refresh(goal)
    
    return goal


def delete_goal(db: Session, goal_id: int, user_id: int) -> bool:
    """
    Delete a goal (soft delete by setting status to 'deleted' or hard delete).
    
    Args:
        db: Database session
        goal_id: Goal ID
        user_id: User ID (to verify ownership)
    
    Returns:
        True if deleted, False if not found
    
    Raises:
        HTTPException: If goal doesn't belong to user
    """
    goal = get_goal(db, goal_id, user_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(goal)
    db.commit()
    
    return True

