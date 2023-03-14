from django.db import models


# Create your models here.
from Classroom.models import Classroom


class Reservation(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    lesson = models.IntegerField()
    teacher = models.CharField(max_length=30)

    class Meta:
        unique_together = ("date", "lesson", "classroom")
        db_table = "Reservations"

    def __str__(self):
        return f'{self.date} {self.classroom} {self.lesson} {self.teacher}'
