# Create your models here.
from django.db import models


class Classroom(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    position = models.CharField(max_length=30)
    interactive_board = models.BooleanField()
    teacher_pc = models.BooleanField()
    teacher_notebook = models.BooleanField()
    flip_chart = models.BooleanField()
    sink = models.BooleanField()
    data_projector = models.BooleanField()
    ethernet_cable = models.BooleanField()

    class Meta:
        db_table = "Classrooms"

    def __str__(self):
        return f'{self.name} {self.position}'

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "interactive_board": self.interactive_board,
            "teacher_pc": self.teacher_pc,
            "teacher_notebook": self.teacher_notebook,
            "flip_chart": self.flip_chart,
            "sink": self.sink,
            "data_projector": self.data_projector,
            "ethernet_cable": self.ethernet_cable,
        }
