# VeganAI Coach

VeganAI Coach is a personal AI cooking assistant designed to help you learn vegan (and occasional pescatarian) recipes while improving your kitchen skills. The project starts small and is meant to grow into a full AWS-backed portfolio showing end-to-end AI engineering and MLOps.

## Vision
- **Learn from your cooking**: Upload photos, notes, ratings, and adjustments after each session so the system can extract structured insights (ingredients, techniques, difficulty, outcomes).
- **Plan your learning**: Set weekly goals like “Master dough hydration control,” track progress, and get suggested next skills.
- **Recommend recipes**: Filter by dietary rules (vegan + optional pescatarian), available ingredients, time, and skill level.
- **Run on AWS**: Use S3 for assets, DynamoDB for knowledge, Lambda for agents, Bedrock/OpenAI for LLMs, CloudWatch for metrics, and Amplify or a lightweight web front-end.

## Current state
- Minimal RAG pipeline using LangChain, Chroma, and OpenAI to answer cooking questions from a seeded text file.
- Simple FastAPI service (`/ask`) with a playful, sarcastic assistant persona.
- CLI scripts to ingest data and query the knowledge base locally.

## Project structure
```
app/
  ingest.py   # Loads sample recipe text, chunks, embeds, and stores in Chroma.
  ask.py      # CLI helper to query the vector store with the sarcastic chef persona.
  main.py     # FastAPI app exposing a health check and /ask endpoint.
data/
  receta_prueba.txt  # Sample recipe text used for the initial knowledge base.
Dockerfile    # Basic container setup for the API.
requirements.txt # Python dependencies (LangChain, FastAPI, OpenAI, etc.).
```

## Getting started locally
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   Create a `.env` file in the project root with your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-...
   ```

3. **Ingest the sample data**
   ```bash
   python app/ingest.py
   ```
   This loads `data/receta_prueba.txt`, chunks it, and writes embeddings to `chroma_db/`.

4. **Query the assistant via CLI**
   ```bash
   python app/ask.py "¿Cómo ajusto la hidratación de la masa?"
   ```

5. **Run the API**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - Health check: `GET /` returns a simple status message.
   - Ask endpoint: `POST /ask` with JSON `{ "question": "..." }`.

## Docker quickstart
Build and run the API inside a container (after creating `.env`):
```bash
docker build -t veganai-coach .
docker run --env-file .env -p 8000:8000 veganai-coach
```

## Roadmap ideas
- Front-end for mobile-friendly recipe browsing and skill tracking.
- Photo and note upload pipeline with vision models to extract structured cooking data.
- Personalized skill plans with weekly goals and progress dashboards.
- Ingredient- and time-aware recipe recommendations.
- AWS deployment: S3 (assets), DynamoDB (user knowledge), Lambda (agents), API Gateway, Bedrock/OpenAI, CloudWatch metrics, and an Amplify-hosted UI.
- CI/CD, infra-as-code (Terraform/CloudFormation), and observability hooks.

## Learning goals
This project is meant to practice:
- Building RAG systems with modern LangChain patterns.
- Designing data flows for personal knowledge bases.
- Deploying serverless AI services on AWS end to end.
- Monitoring, testing, and iterating safely as features grow.
