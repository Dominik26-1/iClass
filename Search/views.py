from datetime import datetime

from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from Classroom.classroom_enum import Classroom_filters
from Classroom.equipment_enum import Equipment
from Utils.python.result.logic_functions import get_day_records, filter_lesson_records, merge_lessons_records, \
    filter_room_records, filter_room_equipment_records
from Utils.python.result.result_functions import build_results_by_room, build_results_by_lesson, build_free_rooms, \
    build_free_room_by_lessons

'''
class DailySearchView(APIView):

    def get(self, request, *args, **kwargs):
        # search/daily/?date=2023-02-27
        str_date = request.query_params[Classroom_filters.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()

        timetable_lessons, sub_lessons = get_day_records(date)
        results = merge_lessons_records(timetable_lessons, sub_lessons, date)
        return Response(build_results_by_room(results))


class DailyRoomSearchView(APIView):

    def get(self, request, *args, **kwargs):
        # search/classroom/?date=2023-02-27&classroom=1
        str_date = request.query_params.get(Classroom_filters.DATE.value)
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        room_id = int(request.query_params[Classroom_filters.CLASSROOM_ID.value])

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_room_records(timetable_lessons, sub_lessons, room_id)

        results = merge_lessons_records(timetable_results, sub_results, date)

        return Response(build_results_by_lesson(results))


class DailyLessonSearchView(APIView):

    def get(self, request, *args, **kwargs):
        # search/classrooms/?date=2023-03-17&lesson=1
        str_date = request.query_params[Classroom_filters.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        lesson = int(request.query_params[Classroom_filters.LESSON.value])

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)

        results = merge_lessons_records(timetable_results, sub_results, date)
        return Response(build_results_by_room(results))


class DailyRoomLessonView(APIView):

    def get(self, request, *args, **kwargs):
        # search/lesson/?date=2023-03-17&lesson=1&classroom=1
        str_date = request.query_params[Classroom_filters.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        lesson = int(request.query_params[Classroom_filters.LESSON.value])
        room_id = int(request.query_params[Classroom_filters.CLASSROOM_ID.value])

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)
        timetable_results, sub_results = filter_room_records(timetable_results, sub_results, room_id)

        results = merge_lessons_records(timetable_results, sub_results, date)
        return Response((len(results) == 0, results))


class DailyMetRoomsView(APIView):

    def get(self, request, *args, **kwargs):
        # search/fitted_classrooms/?date=2023-03-17&teacher_pc=1&data_projector=1
        str_date = request.query_params[Classroom_filters.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        equipment_args = {}
        for key, value in list(request.query_params.items()):
            if key in [eq.value for eq in Equipment]:
                equipment_args[key] = value == "1"

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_room_equipment_records(timetable_lessons, sub_lessons, equipment_args)

        results = merge_lessons_records(timetable_results, sub_results, date)
        return Response(build_free_room_by_lessons(results, equipment_args))


class DailyLessonMetRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # search/fitted_classrooms_lesson/?date=2023-03-17&lesson=1&teacher_pc=1&data_projector=1
        str_date = request.query_params[Classroom_filters.DATE.value]
        lesson = int(request.query_params[Classroom_filters.LESSON.value])
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        equipment_args = {}
        for key, value in list(request.query_params.items()):
            if key in [eq.value for eq in Equipment]:
                equipment_args[key] = value == "1"

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)
        timetable_results, sub_results = filter_room_equipment_records(timetable_results, sub_results, equipment_args)

        results = merge_lessons_records(timetable_results, sub_results, date)
        context = build_free_rooms(results, equipment_args)
        return render(request, "search_form.html", context)
'''

class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})
