from django.urls import path
from .views import chat_messages, chat_forms

app_name= "chatbot"

urlpatterns = [
    path("messages", chat_messages, name="chat_message"),
    path("form",chat_forms, name="chat_form"),
]
