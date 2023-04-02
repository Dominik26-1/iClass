# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from Classroom.models import Classroom
from Core.functions import is_classroom_available
from Edupage.views import parse_inputs
from Reservation.models import Reservation


class ReservationBaseView(View):
    model = Reservation
    fields = '__all__'


class ReservationListView(View):
    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args):
        teacher = f'{request.user.first_name} {request.user.last_name}'
        if request.user.is_superuser:
            reservations = Reservation.objects.all().order_by('date')
        else:
            reservations = Reservation.objects.filter(teacher=teacher).order_by('date')

        context = {
            "reservations": reservations
        }
        return render(request, "reservation_list.html", context)


class ReservationCreateView(View):
    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        input_date, input_lesson, input_room_id, _, parsing_error = parse_inputs(
            REST_method=request.GET)
        if not parsing_error["is_valid"]:
            messages.error(request, parsing_error["errors"][0])
            return redirect('search')
        if (input_date is None) or (input_lesson is None) or (input_room_id is None):
            messages.error(request, "Chýbajúce argumenty (dátum, učebňa alebo hodina) pre rezerváciu učebne.")
            return redirect('search')
        teacher = f'{request.user.first_name} {request.user.last_name}'
        classroom = None
        try:
            classroom = Classroom.objects.get(id=input_room_id)
        except Classroom.DoesNotExist:
            messages.error(request, f"Učebňa s id {input_room_id} neexistuje.")
            redirect('search')
        reservation_candidate = Reservation(classroom=classroom, date=input_date, lesson=input_lesson,
                                            teacher=teacher)
        context = {
            "result": reservation_candidate,
            "action": "create"
        }
        return render(request, "reservation_form.html", context)

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        input_date, input_lesson, input_room_id, _, parsing_error = parse_inputs(
            REST_method=request.POST)
        if not parsing_error["is_valid"]:
            messages.error(request, parsing_error["errors"][0])
            return redirect('search')
        if (input_date is None) or (input_lesson is None) or (input_room_id is None):
            messages.error(request, "Chýbajúce argumenty (dátum, učebňa alebo hodina) pre rezerváciu učebne.")
            return redirect('search')
        teacher = f'{request.user.first_name} {request.user.last_name}'
        is_available, search_errors = is_classroom_available(input_date, input_lesson, input_room_id)
        if not search_errors["is_valid"]:
            messages.error(request, parsing_error["errors"][0])
            return redirect('search')
        if is_available:
            classroom = None
            try:
                classroom = Classroom.objects.get(id=input_room_id)
            except Classroom.DoesNotExist:
                messages.success(request, f"Učebňa s id {input_room_id} neexistuje.")
                redirect('search')
            Reservation.objects.create(date=input_date, classroom=classroom, lesson=input_lesson, teacher=teacher)
            return redirect("reservation-list")
        else:
            messages.error(request, "Učebňa už nie je voľná pre Vami zadaný deň a hodinu.")
            return redirect("search")


class ReservationDeleteView(ReservationBaseView, View):

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        reserved_id = request.POST.get("reservation_id")
        teacher = f'{request.user.first_name} {request.user.last_name}'
        try:
            reservation = Reservation.objects.get(id=reserved_id)
            if reservation.teacher != teacher and not request.user.is_superuser:
                messages.error(request, f"Nedostatočné oprávnenie vymazať rezerváciu s id {id}.")
                return redirect('reservation-list')
            reservation.delete()
        except Reservation.DoesNotExist:
            messages.error(request, f"Rezervácia s {id} neexistuje.")
            return redirect('reservation-list')

        return redirect('reservation-list')


class ReservationDetailView(ReservationBaseView, View):
    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get("id")
        except TypeError:
            messages.error(request, "Chýbajúci parameter id pre rezerváciu.")
            return redirect('reservation-list')
        try:
            reservation = Reservation.objects.get(id=id)
            teacher = f'{request.user.first_name} {request.user.last_name}'
            if reservation.teacher != teacher and not request.user.is_superuser:
                messages.error(request, f"Nedostatočné oprávnenie na prezretie rezervácie s id {id}.")
                return redirect('reservation-list')
        except Reservation.DoesNotExist:
            messages.error(request, f"Rezervácia s {id} neexistuje.")
            return redirect('reservation-list')
        context = {
            "result": reservation,
            "action": "delete"
        }
        return render(request, "reservation_form.html", context)
