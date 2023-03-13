# Create your models here.
import uuid

from django.db import models

from Classroom.models import Classroom
from Timetable.models import Timetable


class Substitution(models.Model):
    id = models.IntegerField(primary_key=True, default=uuid.uuid4().int)
    date = models.DateField(blank=True, null=True)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    new_class = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)
    new_lesson = models.IntegerField(blank=True, null=True)
    new_subject = models.CharField(max_length=30, blank=True, null=True)
    new_teacher = models.CharField(max_length=30, blank=True, null=True)

    if id is None:
        id = uuid.uuid4().int

    class Meta:
        unique_together = ("date", "timetable")
        db_table = "Substitutions"

    def __str__(self):
        return f'{self.new_date} {self.timetable} {self.new_class} {self.new_teacher}'
