from django.urls import path

from Edupage.views import SearchView

urlpatterns = [
    path('', SearchView.as_view()),
]
