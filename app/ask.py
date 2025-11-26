import os
import sys
from dotenv import load_dotenv

# Importaciones de LangChain
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Cargar API Key
load_dotenv()

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../chroma_db")

def main():
    # 1. Recibir pregunta del usuario (argumento de consola o input)
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = input("🧑‍🍳 Pregunta al Chef AI: ")

    print(f"\n🔍 Buscando respuesta para: '{query}'...\n")

    # 2. Conectar a la Base de Datos EXISTENTE (Modo Lectura)
    # IMPORTANTE: Usamos la misma función de embedding que en la ingesta
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    # 3. Crear el Retriever (El "Buscador")
    # search_kwargs={"k": 2} significa "tráeme los 2 fragmentos más relevantes"
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # 4. Configurar el Cerebro (LLM)
    # Usamos gpt-4o-mini porque es rápido, barato y muy listo
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 5. El Prompt del Sistema (Instrucciones de personalidad)
    system_prompt = (
        "Eres un asistente de cocina experto y sarcástico llamado 'VeganAI'. "
        "Usa el siguiente contexto recuperado para responder a la pregunta. "
        "Si la respuesta no está en el contexto, di que no lo sabes, no inventes. "
        "\n\n"
        "Contexto: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # 6. Crear la Cadena (The Chain)
    # "Stuff" chain significa: mete todos los documentos encontrados dentro del prompt
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # 7. Ejecutar
    response = rag_chain.invoke({"input": query})

    # Mostrar resultado
    print("🤖 RESPUESTA:")
    print("-" * 30)
    print(response["answer"])
    print("-" * 30)
    
    # Debug: Ver qué documentos usó realmente (Fuente)
    print("\n📚 Fuente utilizada:")
    for doc in response["context"]:
        print(f"- {doc.page_content[:100]}...")

if __name__ == "__main__":
    main()