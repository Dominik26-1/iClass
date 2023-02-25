from rest_framework import serializers

from Classroom.models import Classroom


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    model = Classroom

    class Meta:
        model = Classroom
        fields = "__all__"
