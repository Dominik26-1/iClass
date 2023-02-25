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
from django.urls import path
from rest_framework import routers

from Classroom.views import ClassroomView
from Substitution.views import SubstitutionView
from Timetable.views import TimetableView
from global_views import DailySearchView, DailyRoomSearchView, DailyLessonSearchView, DailyRoomLessonView, \
    DailyMetRoomsView, DailyLessonMetRoomsView, EdupageView

router = routers.DefaultRouter()
router.register(r'classroom', ClassroomView)

router.register(r'timetable', TimetableView)
router.register(r'substitution', SubstitutionView)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('dailySearch/', DailySearchView.as_view()),
    path('roomSearch/', DailyRoomSearchView.as_view()),
    path('edupage/', EdupageView.as_view()),
    path('lessonSearch/', DailyLessonSearchView.as_view()),
    path('roomLessonSearch/', DailyRoomLessonView.as_view()),
    path('fittedRoomsSearch/', DailyMetRoomsView.as_view()),
    path('fittedRoomsLessonSearch/', DailyLessonMetRoomsView.as_view())
]
'''urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'debug', include(debug_toolbar.urls))

]'''
urlpatterns += router.urls
