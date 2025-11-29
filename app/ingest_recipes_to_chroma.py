"""
Ingest recipes from SQL database into ChromaDB for RAG search.
Run: python -m app.ingest_recipes_to_chroma
"""
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from app.database import SessionLocal
from app.db_models import Recipe

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "../chroma_db")


def create_recipe_document(recipe: Recipe) -> Document:
    """Convert a Recipe from SQL DB to a LangChain Document"""
    # Create a formatted text representation of the recipe
    recipe_text = f"""
RECIPE: {recipe.title}

CUISINE: {recipe.metadata_json.get('cuisine', 'Unknown')}
DIFFICULTY: {recipe.metadata_json.get('difficulty', 'Unknown')}
PREP TIME: {recipe.metadata_json.get('prep_time', 'Unknown')}
COOK TIME: {recipe.metadata_json.get('cook_time', 'Unknown')}

INGREDIENTS:
{recipe.ingredients}

INSTRUCTIONS:
{recipe.instructions}
"""
    
    # Create document with metadata
    return Document(
        page_content=recipe_text.strip(),
        metadata={
            "recipe_id": recipe.id,
            "title": recipe.title,
            "cuisine": recipe.metadata_json.get("cuisine", "Unknown"),
            "difficulty": recipe.metadata_json.get("difficulty", "Unknown"),
            "created_by_ai": recipe.created_by_ai,
        }
    )


def ingest_recipes_to_chroma():
    """Load recipes from SQL DB and ingest them into ChromaDB"""
    print("🚀 Iniciando ingesta de recetas a ChromaDB...")
    
    # 1. Load recipes from SQL database
    db = SessionLocal()
    try:
        recipes = db.query(Recipe).all()
        print(f"📚 Encontradas {len(recipes)} recetas en la base de datos SQL")
        
        if len(recipes) == 0:
            print("❌ No hay recetas para ingerir. Ejecuta seed_recipes.py primero.")
            return
        
        # 2. Convert recipes to LangChain Documents
        documents = []
        for recipe in recipes:
            doc = create_recipe_document(recipe)
            documents.append(doc)
            print(f"  ✅ Preparada: {recipe.title}")
        
        print(f"\n📄 Total documentos preparados: {len(documents)}")
        
    finally:
        db.close()
    
    # 3. Split documents into chunks (for better RAG retrieval)
    print("\n✂️  Dividiendo documentos en chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Larger chunks for recipes (they're self-contained)
        chunk_overlap=100,    # Overlap to maintain context
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"📦 Generados {len(chunks)} chunks")
    
    # 4. Create embeddings and store in ChromaDB
    print("\n🧠 Generando embeddings y guardando en ChromaDB...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # If ChromaDB exists, we'll add to it. If not, create new.
    if os.path.exists(CHROMA_DB_PATH):
        # Load existing ChromaDB
        vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
        # Add new documents
        vector_store.add_documents(chunks)
        print(f"➕ Agregados {len(chunks)} chunks a ChromaDB existente")
    else:
        # Create new ChromaDB
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        print(f"✨ Creada nueva ChromaDB con {len(chunks)} chunks")
    
    # ChromaDB persists automatically, no need to call persist()
    
    print("\n✅ ¡Éxito! Recetas ingeridas en ChromaDB")
    print(f"   ChromaDB ubicada en: {CHROMA_DB_PATH}")
    print(f"   Total chunks indexados: {len(chunks)}")
    print("\n💡 Ahora el sistema RAG puede buscar recetas por similitud semántica")


if __name__ == "__main__":
    ingest_recipes_to_chroma()

