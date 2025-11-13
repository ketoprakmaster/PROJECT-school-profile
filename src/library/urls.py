from django.shortcuts import HttpResponse
from django.urls import path

from library import views

urlpatterns = [
    path("", views.temp)
]
