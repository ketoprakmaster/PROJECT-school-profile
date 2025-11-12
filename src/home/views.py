from django.shortcuts import render

def schedule_view(request):
    """
    A standard Django view to render the schedule page.
    """
    # Context can be added here in the future
    context = {}
    return render(request, "administration/schedule_page.html", context)


def calendar_view(request):
    """
    A standard Django view to render the calendar page.
    """
    # Context can be added here in the future
    context = {}
    return render(request, "administration/calendar_page.html", context)
