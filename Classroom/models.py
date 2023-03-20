# Create your models here.
from django.db import models

from Classroom.equipment_enum import Equipment


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
            "equipment": {
                Equipment.INTERACTIVE_BOARD.value[1]: self.interactive_board,
                Equipment.PC.value[1]: self.teacher_pc,
                Equipment.NOTEBOOK.value[1]: self.teacher_notebook,
                Equipment.FLIP_CHART.value[1]: self.flip_chart,
                Equipment.SINK.value[1]: self.sink,
                Equipment.DATA_PROJECTOR.value[1]: self.data_projector,
                Equipment.ETHERNET_CABLE.value[1]: self.ethernet_cable,
            }

        }
