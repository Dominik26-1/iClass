from rest_framework import serializers

from Timetable.models import Timetable


class TimetableSerializer(serializers.HyperlinkedModelSerializer):
    model = Timetable

    class Meta:
        model = Timetable
        fields = "__all__"
