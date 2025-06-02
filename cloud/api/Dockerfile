# Build stage
FROM python:3.12-slim

WORKDIR /app

# Copiamos requirements primero para aprovechar cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos código API
COPY main.py .

# (opcional) Copiar también carpeta `models` para reutilizar el mismo Event
# COPY ../../models ./models

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
