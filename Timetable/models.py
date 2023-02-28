# Create your models here.
from django.db import models

from App.data_types import DAYS_OF_WEEK
from Classroom.models import Classroom


class Timetable(models.Model):
    id = models.BigAutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=30)
    student_group = models.CharField(max_length=30, blank=True, null=True)
    subject = models.CharField(max_length=30)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    lesson = models.IntegerField()
    teacher = models.CharField(max_length=30)
    is_actual = models.BooleanField(default=True)

    class Meta:
        unique_together = ("lesson", "day", "student_group", "student_class")
        db_table = "Timetables"

    def __str__(self):
        return f'{self.day} {self.student_class} {self.classroom.name}'
