from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import SalaChat, Mensaje
import stomp
import json

def publicar_mensaje_broker(sala_id, mensaje_data):
    # Conexión al broker usando configuración desde settings.py
    host = getattr(settings, 'ACTIVEMQ_HOST', 'broker_mensajeria')
    port = getattr(settings, 'ACTIVEMQ_PORT', 61613)
    conn = stomp.Connection([(host, port)])
    conn.connect('admin', 'admin', wait=True)
    
    # Enviamos el mensaje al tópico de la sala
    topic = f'/topic/chat.{sala_id}'
    conn.send(body=json.dumps(mensaje_data), destination=topic)
    conn.disconnect()

@login_required
def chat_index(request):
    # Página principal de chat que carga la lista de conversaciones
    return render(request, 'chat/index.html')


@login_required
def lista_chats_partial(request):
    """
    Retorna solo el fragmento de la lista de chats.
    """
    if request.user.is_medico:
        # Filtra chats donde el médico sea el de la cita
        chats = SalaChat.objects.filter(cita__agenda__medico__usuario=request.user)
    else:
        # Filtra chats donde el paciente sea el dueño de la cita
        chats = SalaChat.objects.filter(cita__paciente__usuario=request.user)

    return render(request, 'chat/partials/lista_chats.html', {'chats': chats})

@login_required
def detalle_chat_partial(request, sala_id):
    # Buscamos la sala, pero asegurándonos de que el usuario tenga acceso (seguridad)
    sala = get_object_or_404(SalaChat, id=sala_id)
    
    # Validamos acceso: O es el médico de la cita o es el paciente de la cita
    if not (request.user == sala.cita.agenda.medico.usuario or request.user == sala.cita.paciente.usuario):
        return render(request, 'chat/partials/error.html', {'mensaje': 'No tienes acceso a este chat.'})
        
    mensajes = sala.mensajes.all().order_by('fecha_envio')
    
    return render(request, 'chat/partials/mensajes.html', {
        'sala': sala,
        'mensajes': mensajes
    })

@login_required
def enviar_mensaje(request, sala_id):
    if request.method == "POST":
        contenido = request.POST.get('contenido')
        sala = SalaChat.objects.get(id=sala_id)

        # Guardamos el mensaje
        mensaje = Mensaje.objects.create(
            sala=sala,
            remitente=request.user,
            contenido=contenido
        )

        data = {
            'remitente': request.user.username,
            'contenido': mensaje.contenido,
            'fecha': mensaje.fecha_envio.strftime("%H:%M")
        }
        publicar_mensaje_broker(sala_id, data)

        # Reutilizamos la lógica del detalle para devolver la lista actualizada
        # Así el HTMX "swapea" el contenedor con los mensajes nuevos
        return detalle_chat_partial(request, sala_id)
    return HttpResponse(status=405)
