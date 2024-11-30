from django.urls import path
from . import views


urlpatterns = [
    # Chat URLs
    path('chats/', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_read, name='chat_read'),
    path('chat/create-or-get/<int:other_user_id>/', views.create_or_get_chat, name='create_or_get_chat'),
    path('chat/delete/<int:chat_id>/', views.delete_chat, name='delete_chat'),
    path('chat/<int:chat_id>/edit-message/<int:message_id>/', views.edit_message, name='edit_message'),
]
