# 1. Imagen Base: Usamos Python 3.11 ligero (Slim)
FROM python:3.11-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar las dependencias primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# 4. Instalar librerías
# --no-cache-dir reduce el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código (excluyendo .env que se montará como volumen)
# OJO: En producción real, la DB no se copia así, se monta como volumen.
# Pero para este MVP está perfecto.
COPY . .
# Note: .env file should be mounted as volume or passed via env_file in docker-compose

# 6. Exponer el puerto 8080 (El estándar de AWS App Runner/Cloud Run)
EXPOSE 8080

# 7. Comando de arranque: Run migrations then start server
# Note: In production, you might want to run migrations separately
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"