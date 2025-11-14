# school/urls.py
from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path('get/', views.schedule_search, name='schedule-search'),

]
