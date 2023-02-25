from rest_framework import serializers

from Substitution.models import Substitution


class SubstitutionSerializer(serializers.HyperlinkedModelSerializer):
    model = Substitution

    class Meta:
        model = Substitution
        fields = "__all__"
