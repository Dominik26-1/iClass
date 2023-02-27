from django.urls import path

from Edupage.views import EdupageView
from Search.views import DailyLessonSearchView, DailyRoomLessonView, DailyMetRoomsView, DailyLessonMetRoomsView, \
    DailySearchView, DailyRoomSearchView

urlpatterns = [
    path('classrooms/', DailyLessonSearchView.as_view()),
    path('lesson/', DailyRoomLessonView.as_view()),
    path('fitted_classrooms/', DailyMetRoomsView.as_view()),
    path('fitted_classrooms_lesson/', DailyLessonMetRoomsView.as_view()),
    path('daily/', DailySearchView.as_view()),
    path('classroom/', DailyRoomSearchView.as_view()),
    path('edupage/', EdupageView.as_view()),
]
