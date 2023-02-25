from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from Classroom.models import Classroom
from Classroom.serializers import ClassroomSerializer


class ClassroomView(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
