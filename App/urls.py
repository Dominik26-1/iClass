"""App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Classroom-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from Authentication.views import LoginView, LogoutView
from Search.views import HomeView

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('home', HomeView.as_view(), name='home'),
    path('search/', include("Edupage.urls")),
    path('reservations/', include("Reservation.urls"))
]
'''urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'debug', include(debug_toolbar.urls))

]'''
urlpatterns += router.urls
