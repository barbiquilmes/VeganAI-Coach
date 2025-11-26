import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain imports
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = FastAPI(title="VeganAI Coach API")

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

@app.get("/")
def read_root():
    return {"status": "VeganAI is online and hungry 🥕"}

@app.post("/ask")
def ask_chef(request: QueryRequest):
    """Endpoint para preguntar al chef"""
    try:
        response = chain.invoke({"input": request.question})
        return {
            "answer": response["answer"],
            "source_used": [doc.page_content[:50] for doc in response["context"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))