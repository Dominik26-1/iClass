# Create your models here.
import uuid

from django.db import models
from django.db.models import Q

from App.constants import DAYS_OF_WEEK
from Classroom.models import Classroom


class Timetable(models.Model):
    id = models.IntegerField(primary_key=True, default=uuid.uuid4().int)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=30)
    student_group = models.CharField(max_length=30, blank=True, null=True)
    subject = models.CharField(max_length=30)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    lesson = models.IntegerField()
    teacher = models.CharField(max_length=30)
    valid_from = models.DateField()
    valid_to = models.DateField(default=None, blank=True, null=True)

    if id is None:
        id = uuid.uuid4().int

    class Meta:
        unique_together = ("lesson", "day", "student_group", "student_class", "valid_from")
        db_table = "Timetables"

        constraints = [
            models.CheckConstraint(
                check=Q(valid_to__isnull=True) | Q(valid_to__gte=models.F('valid_from')),
                name='kontrola_datumu_prekryvania'
            ),
        ]

    def __str__(self):
        return f'{self.day} {self.student_class} {self.classroom.name}'
