# Create your views here.
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from Reservation.models import Reservation


class ReservationBaseView(View):
    model = Reservation
    fields = '__all__'


class ReservationListView(ReservationBaseView, ListView):
    template_name = "reservation_list.html"
    """View to list all films.
    Use the 'film_list' variable in the template
    to access all Film objects"""


class ReservationDetailView(ReservationBaseView, DetailView):
    """View to list the details from one film.
    Use the 'film' variable in the template to access
    the specific film here and in the Views below"""


class ReservationCreateView(ReservationBaseView, CreateView):
    """View to create a new film"""


class ReservationUpdateView(ReservationBaseView, UpdateView):
    """View to update a film"""


class ReservationDeleteView(ReservationBaseView, DeleteView):
    """View to delete a film"""
