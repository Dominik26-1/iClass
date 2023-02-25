# Create your views here.
from rest_framework import viewsets

from Timetable.models import Timetable
from Timetable.serializers import TimetableSerializer


class TimetableView(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
