FROM python:3.10-slim

WORKDIR /app

# Desactivar buffering de salida y archivos .pyc en disco
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación web
COPY app.py /app/

# Exponer puerto de Streamlit
EXPOSE 8501

# Comando para arrancar el servidor web de Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
