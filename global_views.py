# Create your views here.
from datetime import datetime, date
from itertools import chain

from django.db.models import F
from django.shortcuts import render
from edupage_api.exceptions import BadCredentialsException
from rest_framework.response import Response
from rest_framework.views import APIView

from Classroom.attributes_enum import Classroom_attributes, Equipment
from Classroom.models import Classroom
from Substitution.models import Substitution
from Timetable.models import Timetable

MAX_LESSON = 8


def build_results_by_room(results):
    classrooms = Classroom.objects.all()
    room_results = {}
    for room in classrooms:
        room_results[room.id] = (room.get_dict(), list(filter(lambda less: less["class_room_id"] == room.id, results)))
    return room_results


def build_results_by_lesson(results):
    room_results = {}
    for lesson in range(MAX_LESSON + 1):
        room_results[lesson] = list(filter(lambda less: less["school_lesson"] == lesson, results))
    return room_results


def build_free_room_by_lessons(results, filters):
    room_results = {}
    all_matched_rooms = get_room_candidates_by_filter(filters)
    for lesson in range(MAX_LESSON + 1):
        for room in all_matched_rooms:
            if not list(filter(lambda less: (less["school_lesson"] == lesson and
                                             less["class_room_id"] == room.id), results)):
                room_results[lesson] = room.get_dict()
    return room_results


def build_free_rooms(results, filters):
    room_results = {}
    all_matched_rooms = get_room_candidates_by_filter(filters)
    for room in all_matched_rooms:
        if not list(filter(lambda less: less["class_room_id"] == room.id, results)):
            room_results[room.id] = room.get_dict()
    return room_results


def merge_lessons_records(regular_lessons, sub_lessons, search_date):
    reg_records = regular_lessons.values(students=F('student_class'), search_teacher=F('teacher'),
                                         class_room=F('classroom__name'),
                                         class_room_id=F('classroom__id'),
                                         subject_name=F('subject'),
                                         school_lesson=F('lesson'))
    for rec in reg_records:
        rec["date"] = search_date
    sub_records = sub_lessons.values(students=F('timetable__student_class'),
                                     search_teacher=F('new_teacher' or 'timetable__teacher'),
                                     class_room=F('new_class__name'),
                                     class_room_id=F('new_class__id'),
                                     subject_name=F('new_subject' or 'timetable__subject'),
                                     school_lesson=F('new_lesson'))

    for rec in sub_records:
        rec["date"] = search_date

    return list(chain(reg_records, sub_records))


def get_day_records(date):
    # nezahrn tie hodiny, ktore odpadli
    sub_lessons = Substitution.objects.filter(date=date).exclude(new_lesson=None)
    weekday = date.strftime("%A")
    # nezahrn tie ktore odpadli
    timetable_lessons = Timetable.objects.filter(day=weekday) \
        .exclude(id__in=sub_lessons.values_list('timetable_id'))
    return timetable_lessons, sub_lessons


def filter_lesson_records(timetable_lessons, sub_lessons, lesson):
    return timetable_lessons.filter(lesson=lesson), sub_lessons.filter(new_lesson=lesson)


def filter_room_records(timetable_lessons, sub_lessons, room_id):
    return timetable_lessons.filter(classroom__id=room_id), sub_lessons.filter(new_class__id=room_id)


def filter_room_equipment_records(timetable_lessons, sub_lessons, equipment_filters):
    timetable_filters = {}
    sub_filters = {}
    for key, value in list(equipment_filters.items()):
        timetable_filters[f'classroom__{key}'] = value
        sub_filters[f'new_class__{key}'] = value

    return timetable_lessons.filter(**timetable_filters), sub_lessons.filter(**sub_filters)


def get_room_candidates_by_filter(equipment_filters):
    filters = {}
    for key, value in list(equipment_filters.items()):
        filters[key] = value
        filters[key] = value
    return Classroom.objects.filter(**filters)


class DailySearchView(APIView):

    def get(self, request, *args, **kwargs):
        # dailySearch/?date=2023-02-27
        str_date = request.query_params[Classroom_attributes.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()

        timetable_lessons, sub_lessons = get_day_records(date)
        results = merge_lessons_records(timetable_lessons, sub_lessons, date)
        return Response(build_results_by_room(results))


class DailyRoomSearchView(APIView):

    def get(self, request, *args, **kwargs):
        # roomSearch/?date=2023-02-27&classroom=1
        str_date = request.query_params.get(Classroom_attributes.DATE.value)
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        room_id = int(request.query_params[Classroom_attributes.CLASSROOM_ID.value])

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_room_records(timetable_lessons, sub_lessons, room_id)

        results = merge_lessons_records(timetable_results, sub_results, date)

        return Response(build_results_by_lesson(results))


class DailyLessonSearchView(APIView):

    def get(self, request, *args, **kwargs):
        # lessonSearch/?date=2023-03-17&lesson=1
        str_date = request.query_params[Classroom_attributes.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        lesson = int(request.query_params[Classroom_attributes.LESSON.value])

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)

        results = merge_lessons_records(timetable_results, sub_results, date)
        return Response(build_results_by_room(results))


class DailyRoomLessonView(APIView):

    def get(self, request, *args, **kwargs):
        # roomLessonSearch/?date=2023-03-17&lesson=1&classroom=1
        str_date = request.query_params[Classroom_attributes.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        lesson = int(request.query_params[Classroom_attributes.LESSON.value])
        room_id = int(request.query_params[Classroom_attributes.CLASSROOM_ID.value])

        timetable_lessons, sub_lessons = get_day_records(date)
        timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)
        timetable_results, sub_results = filter_room_records(timetable_results, sub_results, room_id)

        results = merge_lessons_records(timetable_results, sub_results, date)
        return Response((len(results) == 0, results))


class DailyMetRoomsView(APIView):

    def get(self, request, *args, **kwargs):
        # fittedRoomsSearch/?date=2023-03-17&teacher_pc=1&data_projector=1
        str_date = request.query_params[Classroom_attributes.DATE.value]
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

    def get(self, request, *args, **kwargs):
        # fittedRoomsLessonSearch/?date=2023-03-17&lesson=1&teacher_pc=1&data_projector=1
        str_date = request.query_params[Classroom_attributes.DATE.value]
        lesson = int(request.query_params[Classroom_attributes.LESSON.value])
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


class LoginDataParsingException:
    pass


class EdupageView(APIView):

    def get(self, request, *args, **kwargs):
        from edupage_api import Edupage

        edupage = Edupage()

        try:
            edupage.login("JanImrich", "B6TQBWKKTW", subdomain="gta")
        except BadCredentialsException:
            print("Wrong username or password!")
        except LoginDataParsingException:
            print("Try again or open an issue!")
        date = datetime.strptime("2023-02-02", '%Y-%m-%d').date()
        ss = edupage.get_timetable_changes(date)
        for rec in ss:
            print(rec.lesson_n, type(rec.lesson_n))
            student_class = rec.change_class
            '''if type(rec.lesson_n) is int:
                ("lesson", "day", "student_class")
                orig_lesson = Timetable.objects.get(lesson=rec.lesson_n, day=date.strftime("%A"),
                                                    student_class=student_class)
                all_groups = Timetable.objects.values_list("student_group")

                if rec.title.find(':')!= -1:
                    student_group = rec.title.split(':')[0]
                if student_group[0] in all_groups:
                    pass

                Substitution.objects.create(date=date,timetable=orig_lesson, new_class= )
            elif type(rec.lesson_n) is tuple:
                for lesson in range(rec.lesson_n[0],rec.lesson_n[1]+1):

            '''


        with open("out.txt", "a") as f:
            for s in ss:
                f.write(f'{s.change_class},{s.lesson_n},{s.title}')
            pass
        return Response(ss)
