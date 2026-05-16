# Usar una imagen base ligera de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias (optimiza la caché de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app.py .

# Exponer el puerto
EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando para ejecutar el servidor
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]