"""
SQLAlchemy database models for VeganAI Coach.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model - stores basic user information"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    preferences_json = Column(JSON, default={})  # Store general preferences as JSON

    # Relationships
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    recipe_suggestions = relationship("RecipeSuggestion", back_populates="user", cascade="all, delete-orphan")
    recipe_feedback = relationship("RecipeFeedback", back_populates="user", cascade="all, delete-orphan")
    user_preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")


class Goal(Base):
    """Learning goal - e.g., 'Learn 2 recipes per week to master different types of dough'"""
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    target_recipes_per_week = Column(Integer, default=2)
    target_skill = Column(String(100))  # e.g., "dough types", "curries", "desserts"
    status = Column(String(20), default="active")  # active, completed, paused
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="goals")
    paths = relationship("Path", back_populates="goal", cascade="all, delete-orphan")
    recipe_suggestions = relationship("RecipeSuggestion", back_populates="goal", cascade="all, delete-orphan")


class Path(Base):
    """Learning path - steps within a goal"""
    __tablename__ = "paths"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    steps = Column(JSON)  # List of steps as JSON array
    order = Column(Integer, default=0)  # For ordering steps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    goal = relationship("Goal", back_populates="paths")


class Recipe(Base):
    """Recipe model - stores recipe information"""
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    ingredients = Column(Text, nullable=False)  # Can be JSON string or plain text
    instructions = Column(Text, nullable=False)
    created_by_ai = Column(Boolean, default=False)  # True if AI-generated, False if scraped/ingested
    source_url = Column(String(500))  # URL if scraped from web/Instagram
    metadata_json = Column(JSON, default={})  # Additional metadata (difficulty, prep_time, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    recipe_suggestions = relationship("RecipeSuggestion", back_populates="recipe", cascade="all, delete-orphan")
    recipe_feedback = relationship("RecipeFeedback", back_populates="recipe", cascade="all, delete-orphan")


class RecipeSuggestion(Base):
    """Tracks recipe suggestions made to users"""
    __tablename__ = "recipe_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)  # Can be null if not goal-based
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    suggested_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="pending")  # pending, accepted, rejected, completed
    user_comment = Column(Text)  # User's comment when requesting recipe

    # Relationships
    user = relationship("User", back_populates="recipe_suggestions")
    goal = relationship("Goal", back_populates="recipe_suggestions")
    recipe = relationship("Recipe", back_populates="recipe_suggestions")


class RecipeFeedback(Base):
    """User feedback after cooking a recipe"""
    __tablename__ = "recipe_feedback"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    liked = Column(Boolean)
    rating = Column(Integer)  # 1-5 scale
    changes_suggested = Column(Text)  # What user would change
    photo_path = Column(String(500))  # Path to uploaded photo
    ingredients_detected = Column(JSON)  # List of ingredients detected from photo (optional)
    feedback_text = Column(Text)  # General feedback text
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    recipe = relationship("Recipe", back_populates="recipe_feedback")
    user = relationship("User", back_populates="recipe_feedback")


class UserPreference(Base):
    """Learned preferences from user feedback"""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preference_type = Column(String(100), nullable=False)  # e.g., "texture", "spice_level", "salt_level"
    preference_value = Column(Text, nullable=False)  # e.g., "thicker", "less spicy", "more salt"
    learned_from_feedback = Column(Integer, ForeignKey("recipe_feedback.id"), nullable=True)  # Which feedback taught this
    confidence = Column(Float, default=1.0)  # How confident we are in this preference (0-1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="user_preferences")

