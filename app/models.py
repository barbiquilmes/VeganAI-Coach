"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== User Models ==========
class UserCreate(BaseModel):
    """Create a new user"""
    pass  # For now, users are created automatically


class UserResponse(BaseModel):
    """User response model"""
    id: int
    created_at: datetime
    preferences_json: Dict[str, Any]

    class Config:
        from_attributes = True


# ========== Goal Models ==========
class GoalCreate(BaseModel):
    """Create a new learning goal"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    target_recipes_per_week: int = Field(default=2, ge=1, le=10)
    target_skill: Optional[str] = Field(None, max_length=100)


class GoalUpdate(BaseModel):
    """Update an existing goal"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    target_recipes_per_week: Optional[int] = Field(None, ge=1, le=10)
    target_skill: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, pattern="^(active|completed|paused)$")


class GoalResponse(BaseModel):
    """Goal response model"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    target_recipes_per_week: int
    target_skill: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== Path Models ==========
class PathCreate(BaseModel):
    """Create a learning path"""
    goal_id: int
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    steps: Optional[List[str]] = None
    order: int = Field(default=0, ge=0)


class PathResponse(BaseModel):
    """Path response model"""
    id: int
    goal_id: int
    name: str
    description: Optional[str]
    steps: Optional[List[str]]
    order: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Recipe Models ==========
class RecipeCreate(BaseModel):
    """Create a new recipe"""
    title: str = Field(..., min_length=1, max_length=200)
    ingredients: str = Field(..., min_length=1)
    instructions: str = Field(..., min_length=1)
    created_by_ai: bool = False
    source_url: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class RecipeResponse(BaseModel):
    """Recipe response model"""
    id: int
    title: str
    ingredients: str
    instructions: str
    created_by_ai: bool
    source_url: Optional[str]
    metadata_json: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Recipe Suggestion Models ==========
class RecipeSuggestionRequest(BaseModel):
    """Request a recipe suggestion"""
    goal_id: Optional[int] = None
    user_comment: Optional[str] = None  # User's comment about what they want


class RecipeSuggestionResponse(BaseModel):
    """Recipe suggestion response"""
    id: int
    user_id: int
    goal_id: Optional[int]
    recipe_id: int
    suggested_at: datetime
    status: str
    user_comment: Optional[str]
    recipe: RecipeResponse  # Include full recipe details

    class Config:
        from_attributes = True


# ========== Feedback Models ==========
class RecipeFeedbackCreate(BaseModel):
    """Submit feedback for a recipe"""
    liked: Optional[bool] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    changes_suggested: Optional[str] = None
    feedback_text: Optional[str] = None
    ingredients_detected: Optional[List[str]] = None  # From photo analysis


class RecipeFeedbackResponse(BaseModel):
    """Feedback response model"""
    id: int
    recipe_id: int
    user_id: int
    liked: Optional[bool]
    rating: Optional[int]
    changes_suggested: Optional[str]
    photo_path: Optional[str]
    ingredients_detected: Optional[List[str]]
    feedback_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== User Preference Models ==========
class UserPreferenceResponse(BaseModel):
    """User preference response model"""
    id: int
    user_id: int
    preference_type: str
    preference_value: str
    learned_from_feedback: Optional[int]
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True

