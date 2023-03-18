from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html", {})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Úspešne Ste boli prihlasený.")
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.success(request, "Prihlásenie zlyhalo. Skontrolujte Vaše prihlasovacie údaje.")
            return redirect('login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
