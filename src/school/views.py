from django.shortcuts import render
from django.db.models import Q
from .models import SubjectSchedule, AcademicCalendar
import time

def schedule_search(request):
    query = request.GET.get("query")
    schedules = None

    if query:
        search_query = Q(class_obj__name__icontains=query) | \
                       Q(teacher__full_name__icontains=query) | \
                       Q(subject__name__icontains=query)

        schedules = SubjectSchedule.objects.filter(search_query)

    context = {
        "query": query,
        "results": schedules
    }

    return render(request, "cotton/schedule/results.html", context)


def schedule_view(request):

    return render(request, "school/schedule_page.html")


def calendar_view(request):
    """
    A standard Django view to render the calendar page.
    """
    events = AcademicCalendar.objects.all()
    context = {
        'events': events
    }

    print(context["events"])
    return render(request, "school/calendar_page.html", context)
