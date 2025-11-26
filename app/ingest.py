import os
from dotenv import load_dotenv

# Importaciones modernas de LangChain (v0.3)
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Cargar variables de entorno (API Key)
load_dotenv()

# Rutas Dinámicas (Para que funcione en tu Mac/Windows y luego en Docker/AWS igual)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/receta_prueba.txt")
DB_PATH = os.path.join(BASE_DIR, "../chroma_db")

def main():
    print("🚀 Iniciando proceso de Ingesta (ETL)...")

    # 1. LOAD: Cargar datos crudos
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: No encuentro el archivo en {DATA_PATH}")
        return
    
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    docs = loader.load()
    print(f"📄 Documento cargado. Caracteres brutos: {len(docs[0].page_content)}")

    # 2. TRANSFORM (Chunking): La parte crítica para RAG
    # Usamos RecursiveCharacterTextSplitter para no romper párrafos ni frases.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # Tamaño del trozo (tokens aprox)
        chunk_overlap=50,     # Solapamiento para mantener contexto entre cortes
        separators=["\n\n", "\n", ".", " "] # Prioridad de corte
    )
    chunks = text_splitter.split_documents(docs)
    print(f"✂️  Generados {len(chunks)} chunks (fragmentos).")

    # 3. TRANSFORM (Embedding) & LOAD (Indexación)
    print("🧠 Generando Embeddings (llamando a OpenAI)...")
    
    # Usamos el modelo 'small' v3: más barato y mejor rendimiento que ada-002
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Chroma hace el trabajo sucio: Embeddea los chunks y los guarda en disco
    if os.path.exists(DB_PATH):
        # Si ya existe, podrías borrarla para empezar de cero, 
        # pero Chroma gestiona actualizaciones.
        print(f"💾 Guardando en base de datos existente en: {DB_PATH}")
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print("✅ ¡Éxito! Base de conocimiento actualizada.")
    print("   Ahora tu IA tiene memoria a largo plazo en tu disco local.")

if __name__ == "__main__":
    main()