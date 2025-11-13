from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path("jadwal/", views.schedule_view, name="schedule-page"),
    path("kalender/", views.calendar_view, name="calendar-page"),
]
