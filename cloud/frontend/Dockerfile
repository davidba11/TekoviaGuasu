FROM python:3.12-slim

# variables de entorno para producción
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# instala paquetes del sistema que necesita Reflex (Node, etc.)
RUN apt-get update \
 && apt-get install -y curl build-essential git \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# compila el frontend y congela el backend
RUN reflex export --no-zip

# la carpeta exporta el site en /app/.web
WORKDIR /app/.web

# arrancamos con un servidor estático simple (ej. vite preview o http.server)
CMD ["python", "-m", "http.server", "3000"]
