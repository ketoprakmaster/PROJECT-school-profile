from django.contrib import admin
from .models import (
    Subject, Class, ClassRoom, Teacher, ScheduleSlot,
    SubjectSchedule, AcademicCalendar
)

# --- 1. Mendaftarkan Entitas Sederhana ---

# Pendaftaran standar
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(ClassRoom)
admin.site.register(ScheduleSlot)


# --- 2. Kustomisasi Model Teacher ---

class TeacherAdmin(admin.ModelAdmin):
    # Menampilkan kolom-kolom ini di daftar
    list_display = ('full_name', 'employee_id', 'user_account_status')
    # Filter data berdasarkan status user (jika terintegrasi dengan User)
    list_filter = ('user',)
    # Field yang bisa dicari
    search_fields = ('full_name', 'employee_id')

    # Fungsi kustom untuk menampilkan status User
    def user_account_status(self, obj):
        if obj.user:
            return "Aktif" if obj.user.is_active else "Nonaktif"
        return "Tidak Terintegrasi"
    user_account_status.short_description = "Status Akun User"

admin.site.register(Teacher, TeacherAdmin)


# --- 3. Kustomisasi Model Jadwal (SubjectSchedule) ---

class SubjectScheduleAdmin(admin.ModelAdmin):
    # Kolom yang ditampilkan di daftar jadwal
    list_display = (
        'class_obj',
        'day',
        'get_schedule_time', # Panggil method kustom
        'subject',
        'teacher',
        'room'
    )
    # Filter yang sangat penting untuk pencarian jadwal
    list_filter = ('day', 'class_obj', 'teacher', 'subject')
    # Field yang dapat dicari
    search_fields = ('class_obj__name', 'teacher__full_name', 'subject__name')
    # Memastikan Hari (day) dan Slot Waktu (schedule_slot) terurut
    ordering = ('day', 'schedule_slot__start_time')

    # Fungsi kustom untuk menampilkan gabungan waktu
    def get_schedule_time(self, obj):
        return str(obj.schedule_slot)
    get_schedule_time.short_description = "Waktu"

admin.site.register(SubjectSchedule, SubjectScheduleAdmin)


# --- 4. Kustomisasi Model Kalender Akademik ---

class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_start','event_end' ,'description_summary')
    # Filter berdasarkan tahun/bulan
    list_filter = ('event_start',)
    # Urutkan berdasarkan tanggal terdekat
    ordering = ('event_start',)

    def description_summary(self, obj):
        # Tampilkan ringkasan deskripsi (maks. 50 karakter)
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    description_summary.short_description = "Keterangan"

admin.site.register(AcademicCalendar, AcademicCalendarAdmin)
