FROM python:3.10-slim

WORKDIR /backend

# Evitar la escritura de archivos .pyc en disco y habilitar el buffering de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias
COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend
COPY app /backend/app

# Exponer el puerto de la API
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
