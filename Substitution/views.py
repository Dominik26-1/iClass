# Create your views here.
from rest_framework import viewsets

from Substitution.models import Substitution
from Substitution.serializers import SubstitutionSerializer


class SubstitutionView(viewsets.ModelViewSet):
    queryset = Substitution.objects.all()
    serializer_class = SubstitutionSerializer
