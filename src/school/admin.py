from django.contrib import admin
from .models import (
    Subject, Class, ClassRoom, Teacher, ScheduleSlot,
    SubjectSchedule, AcademicCalendar
)


admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(ClassRoom)
admin.site.register(ScheduleSlot)



class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'employee_id', 'user_account_status')
    list_filter = ('user',)
    search_fields = ('full_name', 'employee_id')

    def user_account_status(self, obj):
        if obj.user:
            return "Aktif" if obj.user.is_active else "Nonaktif"
        return "Tidak Terintegrasi"
    user_account_status.short_description = "Status Akun User"

admin.site.register(Teacher, TeacherAdmin)



class SubjectScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'class_obj',
        'day',
        'get_schedule_time', # Panggil method kustom
        'subject',
        'teacher',
        'room'
    )
    list_filter = ('day', 'class_obj', 'teacher', 'subject')
    search_fields = ('class_obj__name', 'teacher__full_name', 'subject__name')
    ordering = ('day', 'schedule_slot__start_time')

    def get_schedule_time(self, obj):
        return str(obj.schedule_slot)
    get_schedule_time.short_description = "Waktu"

admin.site.register(SubjectSchedule, SubjectScheduleAdmin)



class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_start','event_end' ,'description_summary')
    list_filter = ('event_start',)
    ordering = ('event_start',)

    def description_summary(self, obj):
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    description_summary.short_description = "Keterangan"

admin.site.register(AcademicCalendar, AcademicCalendarAdmin)
