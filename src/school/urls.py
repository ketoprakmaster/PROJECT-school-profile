# school/urls.py
from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path('', views.schedule_search, name='schedule-search'),
]
