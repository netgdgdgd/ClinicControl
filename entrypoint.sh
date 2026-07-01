#!/bin/bash

# Salir inmediatamente si algún comando falla
set -e

echo "Esperando a que MariaDB inicie completamente..."
# Un pequeño delay de seguridad para darle tiempo al motor de base de datos de levantar en Windows
sleep 5

echo "Ejecutando migraciones de Django..."
python manage.py makemigrations
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando el servidor de Django..."
# Ejecuta el comando que le pasemos desde el Dockerfile o docker-compose
exec "$@"
