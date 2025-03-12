# chat/urls.py
from django.urls import path
from .views import (
    user_search,
    start_conversation,
    conversation_detail,
    conversation_list
)

urlpatterns = [
    path('search/', user_search, name='user_search'),
    path('conversation/start/<int:user_id>/', start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('conversations/', conversation_list, name='conversation_list'),
]
