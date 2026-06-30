# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Evitar que Python genere archivos .pyc y forzar la salida directa a la terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear y movernos al directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar el driver de MariaDB/MySQL
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalar
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . /app/

# Copiar el entrypoint y darle permisos de ejecución
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto de Django
EXPOSE 8000

# Usar el script como punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# El comando por defecto que recibirá el entrypoint
CMD ["gunicorn", "ClinicControl.wsgi:application", "--bind", "0.0.0.0:8000"]
