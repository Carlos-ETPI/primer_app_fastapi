FROM python:3.11-slim

# Crear usuario de sistema para seguridad
RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código y dar permisos al usuario
COPY --chown=appuser:appgroup . .

USER appuser

# Exponer el puerto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]