from school.models import AcademicCalendar
from wagtail import blocks


class AcademicCalendarBlock(blocks.StructBlock):
    """block for the academic calendars"""
    title = blocks.CharBlock(default="Jadwal Kegiatan Akademik", required=False)
    subtitle = blocks.CharBlock(required=False)
    limit = blocks.IntegerBlock(default=50, required=False)
    show_description = blocks.BooleanBlock(default=False, required=False)
    date_start = blocks.DateBlock(required=False)
    date_end = blocks.DateBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        qs = AcademicCalendar.objects.all() # pyright: ignore
        if value["limit"]:
            qs = qs[:value["limit"]]

        context["events"] = qs
        return context

    class Meta:
        template = "blocks/calendar-section.html"
        icon = "date"
        label = "Academic Calendar"


class ScheduleBlock(blocks.StructBlock):
    """Schedule Block for Searching Schedule"""

    class Meta:
        template = "blocks/schedule-section.html"
        icon = "date"
        label = "schedule search"
