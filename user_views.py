from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView


class RegistrationView(APIView):
    def post(self, request):
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        ss = User.objects.filter(Q(username=username) | Q(email=email))
        if not ss:
            User.objects.create_user(username, email, password)
        else:
            return Response("User already exists", status=400)
        return redirect('/')
