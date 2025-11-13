# school/urls.py
from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path('jadwal/', views.schedule_view, name='schedule-page'),
    path('jadwal/cari/', views.schedule_search, name='schedule-search'),
    path('kalender/', views.calendar_view, name='calendar-page'),

]
