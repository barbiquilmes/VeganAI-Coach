import os
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# LangChain imports
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Database and models
from app.database import get_db
from app.models import (
    UserResponse, GoalCreate, GoalUpdate, GoalResponse,
    RecipeSuggestionRequest
)
from app.services import user_service, goal_service

load_dotenv()

app = FastAPI(
    title="VeganAI Coach API",
    description="AI-powered vegan recipe learning coach",
    version="1.0.0"
)

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../chroma_db")

# Modelo de datos para la petición (Request)
class QueryRequest(BaseModel):
    question: str

# Configuración Global (se carga al arrancar)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Prompt Sarcástico
system_prompt = (
    "Eres un asistente de cocina experto y sarcástico llamado 'VeganAI'. "
    "Usa el siguiente contexto para responder. "
    "Si no sabes, dilo, pero con estilo. "
    "\n\nContexto: {context}"
)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Crear la cadena
chain = create_retrieval_chain(
    retriever,
    create_stuff_documents_chain(llm, prompt_template)
)

# Modelo de datos para la petición (Request) - kept for backward compatibility
class QueryRequest(BaseModel):
    question: str

# ============================================================================
# Health & Info Endpoints
# ============================================================================

@app.get("/")
def read_root():
    """Root endpoint - API status"""
    return {"status": "VeganAI is online and hungry 🥕", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# ============================================================================
# User Endpoints
# ============================================================================

@app.post("/api/users", response_model=UserResponse, tags=["users"])
def create_or_get_user(db: Session = Depends(get_db)):
    """
    Create or get user.
    For MVP, returns the first user or creates one.
    """
    user = user_service.get_or_create_user(db)
    return user


@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ============================================================================
# Goal Endpoints
# ============================================================================

@app.post("/api/goals", response_model=GoalResponse, status_code=201, tags=["goals"])
def create_goal(
    goal_data: GoalCreate,
    user_id: int = 1,  # For MVP, default to user 1. In production, get from auth
    db: Session = Depends(get_db)
):
    """
    Create a new learning goal.
    
    Example:
    {
        "title": "Learn dough types",
        "description": "Master different types of vegan dough",
        "target_recipes_per_week": 2,
        "target_skill": "dough types"
    }
    """
    goal = goal_service.create_goal(db, user_id, goal_data)
    return goal


@app.get("/api/goals", response_model=List[GoalResponse], tags=["goals"])
def list_goals(
    user_id: int = 1,  # For MVP, default to user 1
    status: str = None,  # Optional filter: active, completed, paused
    db: Session = Depends(get_db)
):
    """List all goals for a user, optionally filtered by status"""
    goals = goal_service.get_user_goals(db, user_id, status)
    return goals


@app.get("/api/goals/{goal_id}", response_model=GoalResponse, tags=["goals"])
def get_goal(
    goal_id: int,
    user_id: int = 1,  # For MVP, default to user 1
    db: Session = Depends(get_db)
):
    """Get a specific goal by ID"""
    goal = goal_service.get_goal(db, goal_id, user_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@app.put("/api/goals/{goal_id}", response_model=GoalResponse, tags=["goals"])
def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    user_id: int = 1,  # For MVP, default to user 1
    db: Session = Depends(get_db)
):
    """Update an existing goal"""
    goal = goal_service.update_goal(db, goal_id, user_id, goal_data)
    return goal


@app.delete("/api/goals/{goal_id}", status_code=204, tags=["goals"])
def delete_goal(
    goal_id: int,
    user_id: int = 1,  # For MVP, default to user 1
    db: Session = Depends(get_db)
):
    """Delete a goal"""
    goal_service.delete_goal(db, goal_id, user_id)
    return None


# ============================================================================
# Recipe Q&A Endpoint (Existing)
# ============================================================================

@app.post("/ask", tags=["recipes"])
def ask_chef(request: QueryRequest):
    """Endpoint para preguntar al chef (existing RAG functionality)"""
    try:
        response = chain.invoke({"input": request.question})
        return {
            "answer": response["answer"],
            "source_used": [doc.page_content[:50] for doc in response["context"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))