from django.urls import path
from .views import chat_index, detalle_chat_partial, enviar_mensaje, lista_chats_partial

urlpatterns = [
    path('', chat_index, name='chat_index'),
    path('lista/', lista_chats_partial, name='lista-chats'),
    # El path debe coincidir con la estructura que HTMX llama
    # Si en tu `urls.py` principal (ClinicControl/urls.py) pusiste `path('chat/', include('chat.urls'))`
    # Entonces el path aquí debe ser 'detalle/<int:sala_id>/'
    path('detalle/<int:sala_id>/', detalle_chat_partial, name='chat_detalle'),
    path('enviar/<int:sala_id>/', enviar_mensaje, name='chat_enviar_mensaje'),
]
