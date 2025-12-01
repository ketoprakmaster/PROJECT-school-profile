from django.db import models
from django.contrib.auth.models import User # Asumsi menggunakan User bawaan Django


DAY_CHOICES = (
    ('MONDAY', 'Senin'),
    ('TUESDAY', 'Selasa'),
    ('WEDNESDAY', 'Rabu'),
    ('THURSDAY', 'Kamis'),
    ('FRIDAY', 'Jumat'),
    ('SATURDAY', 'Sabtu'),
)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length= 100, null=True, blank=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=10)
    desc = models.CharField(max_length= 100, null=True, blank=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length= 100, null=True, blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.full_name


class ScheduleSlot(models.Model):
    # Menyimpan jam pelajaran, misalnya (07:00 - 07:45)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}" # pyright: ignore


class SubjectSchedule(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Kelas")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name="Mata Pelajaran")
    schedule_slot = models.ForeignKey(ScheduleSlot, on_delete=models.PROTECT, verbose_name="Slot Waktu")
    room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ruang Kelas")
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name="Guru Pengajar")

    day = models.CharField(
        max_length=10,
        choices=DAY_CHOICES,
        verbose_name="Hari"
    )

    class Meta:
        # Menjamin dalam satu kelas, satu hari, dan satu slot waktu tidak ada mata pelajaran ganda.
        unique_together = ('class_obj', 'day', 'schedule_slot')
        ordering = ['day', 'schedule_slot__start_time']

    def __str__(self):
        return f"{self.class_obj} - {self.day} ({self.subject})"


class AcademicCalendar(models.Model):
    event_name = models.CharField(max_length=255, verbose_name="Nama Acara/Kegiatan")
    event_start = models.DateField(verbose_name="Tanggal")
    event_end = models.DateField(verbose_name="Tanggal", null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Keterangan")

    class Meta:
        ordering = ['event_start']

    def __str__(self):
        return f"{self.event_name}: {self.event_start} - {self.event_end}"
