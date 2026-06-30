# ClinicControl

ClinicControl es una aplicacion clinica web completa dise�ada para ejecutarse con **MariaDB** y mensajeria en tiempo real. El sistema utiliza **ActiveMQ** y **STOMP** para el chat entre medicos y pacientes, y documenta sus APIs con **Swagger**.

## Por que se usa STOMP TCP en este proyecto
- STOMP TCP es el protocolo que usa el backend de Django para publicar mensajes directamente al broker **ActiveMQ**.
- En el proyecto, el servidor Python usa la libreria `stomp.py` para enviar los mensajes de chat al topic de ActiveMQ en el puerto **61613**.
- El frontend web usa `stomp.js` sobre WebSocket para recibir los mensajes en el navegador.
- En resumen: STOMP TCP se usa para la comunicacion servidor -> broker, y STOMP sobre WebSocket se usa para la comunicacion browser -> broker.

## Tecnologias clave
- Backend: Django 4.x
- API: Django REST Framework (DRF)
- Documentacion de API: drf-spectacular / Swagger
- Base de datos: MariaDB
- Mensajeria en tiempo real: ActiveMQ + STOMP
- Cliente de mensajeria web: stomp.js
- Frontend: Bootstrap 5 + HTMX + Django Templates
- Contenerizacion: Docker + Docker Compose
- Servidor de aplicacion: Gunicorn

## Caracteristicas principales
- Registro web de pacientes y medicos con validacion de contrasena
- Autenticacion de usuarios con Django Auth
- Agendamiento de citas medicas
- Generacion automatica de sala de chat por cita
- Mensajeria en tiempo real para medico/paciente usando STOMP
- Swagger UI en `/api/docs/` para explorar APIs
- Ambiente Dockerizado listo para compartir en GitHub

## Requisitos
- Docker
- Docker Compose
- Git
- Fly CLI (`flyctl`) para despliegue rapido en fly.dev

## Estructura del contenedor local
- `db`: MariaDB 10.11
- `activemq`: Broker de mensajeria STOMP / WebSocket
- `web`: Django + Gunicorn

## Configuracion local
1. Copia el archivo de ejemplo:

```bash
type .env.example > .env
```

2. Ajusta `.env` si es necesario.
3. Levanta los servicios:

```bash
docker-compose up -d --build
```

4. El contenedor `web` ejecuta migraciones y collectstatic automaticamente.

## Accesos
- App web: http://localhost:8000
- Swagger docs: http://localhost:8000/api/docs/
- ActiveMQ UI: http://localhost:8161/

## Variables de entorno
El proyecto utiliza `.env` con estas variables principales:

```env
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=mysql://django_user:django_password@db:3306/clinica_db
ACTIVEMQ_HOST=broker_mensajeria
ACTIVEMQ_PORT=61613
```

## Docker Compose y MariaDB
La aplicacion esta dise�ada para ejecutarse exclusivamente con MariaDB a traves de `docker-compose.yml`.
El servicio `db` expone el puerto `3306` y el servicio `web` se conecta usando `DATABASE_URL`.

## Mensajeria en tiempo real
- El broker ActiveMQ esta disponible en `broker_mensajeria`
- El puerto STOMP TCP es `61613`
- El puerto STOMP WebSocket es `61614`
- El cliente web usa `stomp.js` para suscribirse a `/topic/chat.<id>`

## Swagger
La documentacion de APIs esta disponible en:

- `http://localhost:8000/api/docs/`

## Despliegue en fly.dev
Para desplegar en Fly, sigue estos pasos:

1. Instala `flyctl`.
2. Abre una terminal en `src`.
3. Ejecuta:

```bash
fly launch --name cliniccontrol --dockerfile Dockerfile
```

4. Configura los secretos de Fly:

```bash
fly secrets set SECRET_KEY=... DATABASE_URL=... ACTIVEMQ_HOST=... ACTIVEMQ_PORT=61613
```

5. Despliega:

```bash
fly deploy
```

> Nota: en fly.dev se recomienda usar un servicio de base de datos MariaDB administrado y un broker STOMP/ActiveMQ externo, ya que `docker-compose` no se usa en producci�n Fly.

## Pruebas
Ejecuta las pruebas del modulo de usuarios:

```bash
docker-compose exec web python manage.py test usuarios --settings=ClinicControl.settings

docker-compose exec web python manage.py changepassword <username>
```

## Subir a GitHub
Si subes el proyecto a GitHub:
- Asegurate de incluir `src/`, `README.md`, `docker-compose.yml`, `Dockerfile`, `fly.toml`, `.env.example` y el codigo de la app.
- No subas `.env`, archivos de entorno privados o dependencias locales.
- Cualquier companero con Docker y Docker Compose puede clonar el repositorio, copiar `.env.example` a `.env` y ejecutar `docker-compose up -d --build`.
