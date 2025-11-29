# Performance Notes - Endpoint /ask

## ¿Por qué tarda el endpoint `/ask`?

El endpoint `/ask` usa **RAG (Retrieval Augmented Generation)**, que involucra múltiples pasos:

### Proceso RAG:

1. **Embedding de la pregunta** (~0.5-1s)
   - Convierte la pregunta del usuario en un vector
   - Llamada a OpenAI API: `text-embedding-3-small`
   - Latencia de red + procesamiento

2. **Búsqueda vectorial en ChromaDB** (~0.1s)
   - Busca recetas similares en la base vectorial
   - Compara embeddings
   - Retorna los 2 documentos más relevantes

3. **Generación de respuesta con LLM** (~2-5s)
   - Envía contexto + pregunta a GPT-4o-mini
   - El LLM genera la respuesta
   - Latencia de red + tiempo de generación

**Tiempo total esperado: 3-6 segundos**

### Comparación con otros endpoints:

- `/api/goals` → **< 50ms** (solo consulta SQL local)
- `/api/users` → **< 50ms** (solo consulta SQL local)
- `/ask` → **3-6 segundos** (2 llamadas a OpenAI API)

## Optimizaciones posibles:

### 1. **Caching de embeddings** (Ahorro: ~0.5-1s)
```python
# Cachear embeddings de preguntas comunes
from functools import lru_cache
```

### 2. **Reducir documentos recuperados** (Ahorro: ~0.1s)
```python
# Ya estamos usando k=2, que es óptimo
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
```

### 3. **Usar modelo más rápido** (Ahorro: ~1-2s)
```python
# gpt-4o-mini ya es rápido, pero podríamos usar:
# - gpt-3.5-turbo (más rápido pero menos inteligente)
# - Streaming responses (mejora percepción de velocidad)
```

### 4. **Streaming de respuestas** (Mejora percepción)
```python
# Enviar respuesta mientras se genera (chunk por chunk)
# El usuario ve respuesta más rápido
```

### 5. **Timeout y retry logic**
```python
# Agregar timeout para evitar esperas infinitas
# Retry automático si falla
```

### 6. **Async/await** (Mejora concurrencia)
```python
# Permitir múltiples requests simultáneos
# No bloquea el servidor
```

## Monitoreo:

Ahora el endpoint incluye logging de tiempos. Revisa los logs:
```bash
docker-compose logs veganai-coach | grep "⏱️"
```

## Recomendación:

Para MVP, **3-6 segundos es aceptable** para un endpoint que:
- Hace búsqueda semántica
- Genera respuestas inteligentes
- Usa IA

Si necesitas más velocidad, prioriza:
1. ✅ **Streaming** (mejora percepción)
2. ✅ **Caching** (preguntas frecuentes)
3. ✅ **Async** (mejor concurrencia)

