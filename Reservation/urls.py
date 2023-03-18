from django.urls import path

from Reservation.views import *

urlpatterns = [
    path('', ReservationListView.as_view(), name="reservation-list"),
    path('create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('delete/', ReservationDeleteView.as_view(), name="reservation-delete"),
    path('<int:id>/', ReservationDetailView.as_view(), name="reservation-detail"),
]
