from django.urls import path
from .views import chat_hx

app_name= "chatbot"

urlpatterns = [
    path("", chat_hx, name="default"),
]
