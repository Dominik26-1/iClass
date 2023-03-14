from django.urls import path

from Reservation.views import *

urlpatterns = [
    path('', ReservationListView.as_view()),
    path('', ReservationCreateView.as_view()),
    path('<int:id>', ReservationDetailView.as_view()),
    path('<int:id>', ReservationUpdateView.as_view()),
]