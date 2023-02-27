from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html", {})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Succesfully logged in..."))
            return redirect('login')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect('login')


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

