import re
from datetime import datetime
from itertools import chain

from django.shortcuts import render
from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException
from edupage_api.substitution import Action, TimetableChange
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from Classroom.classroom_enum import Classroom_filters
from Classroom.equipment_enum import Equipment
from Substitution.models import Substitution
from Timetable.models import Timetable
from Utils.python.result.logic_functions import merge_lessons_records, filter_room_equipment_records, \
    filter_lesson_records, filter_room_records
from Utils.python.result.result_functions import build_results_by_room, build_free_rooms, build_results_by_lesson, \
    build_free_room_by_lessons

edupage = Edupage()
try:
    edupage.login("JanImrich", "B6TQBWKKTW", subdomain="gta")
except BadCredentialsException:
    print("Wrong username or password!")


def get_day_records(date):
    substitutions = edupage.get_timetable_changes(date)
    sub_lessons = []
    for sub in substitutions:
        if type(sub.lesson_n) is int:
            sub_lessons.extend(parse_edupage_object(sub, sub.lesson_n, date))
        elif type(sub.lesson_n) is tuple:
            for lesson in range(sub.lesson_n[0], sub.lesson_n[1] + 1):
                sub_lessons.extend(parse_edupage_object(sub, lesson, date))
            # nezahrn tie ktore su v suplovani
    timetable_lessons = Timetable.objects.filter(day=date.strftime("%A")).exclude(
        id__in=map(lambda les: les.timetable_id, sub_lessons))
    return list(chain(timetable_lessons)), list(filter(lambda les: les.new_lesson is not None, sub_lessons))


def parse_edupage_object(timetable_change: TimetableChange, orig_lesson: int, date):
    if timetable_change.action == Action.CHANGE:
        regex_match = re.search(
            r'^(?:(?P<student_group>[a-žA-Ž0-9\s\.]+):{1})?(?:\s*\({1}(?P<old_subject>[a-žA-Ž\s]+)\){1}\s*➔{1}\s*)?\s*(?P<new_subject>[a-žA-Ž\s]+)\s+\-{1}\s*(Suplovanie{1}):{1}\s*\({1}(?P<old_teacher>[A-Ža-ž\s]+)[\s)]+➔{1}\s*(?P<new_teacher>[[A-Ža-ž\s]+)',
            timetable_change.title)
        new_lesson_reg = re.search(r'za{1}[^a-žA-Ž0-9]*(?P<moved_lesson>[0-9]{1})\.?.*hod{1}\.?',
                                   timetable_change.title)
        change_room_reg = re.search(
            r'\s*Zameniť učebňu{1}:{1}\s*\({1}(?P<old_room>[a-žA-Ž0-9]+)\){1}\s*➔{1}\s*(?P<new_room>[a-žA-Ž0-9]+)',
            timetable_change.title)
        moved_lesson, old_room, new_room = None, None, None
        if regex_match:
            students_group = regex_match.group("student_group")
            old_subject, new_subject = regex_match.group("old_subject"), regex_match.group("new_subject")
            old_teacher, new_teacher = regex_match.group("old_teacher"), regex_match.group("new_teacher")
            if change_room_reg:
                old_room = change_room_reg.group("old_room")
                new_room = change_room_reg.group("new_room")
            if new_lesson_reg:
                moved_lesson = new_lesson_reg.group("moved_lesson")
                '''moved_reg_les = Timetable.objects.get(lesson=moved_lesson, day=date.strftime("%A"),
                                                      student_class=timetable_change.change_class,
                                                      student_group=students_group)'''
                hod = Timetable.objects.all.first()
                presunuta_hodina = Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                                timetable=hod,
                                                new_subject=None, new_teacher=new_teacher)
                orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                    student_class=timetable_change.change_class,
                                                    student_group=students_group)
                odpadnuta_hodina = Substitution(date=date, new_class=None, new_lesson=None, timetable=orig_record,
                                                new_subject=None, new_teacher=None)
                return [presunuta_hodina, odpadnuta_hodina]
            else:
                '''
                orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                    student_class=timetable_change.change_class,
                                                    student_group=students_group)'''
                hod = Timetable.objects.first()
                return [Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                     timetable=hod,
                                     new_subject=new_subject, new_teacher=new_teacher)]
    elif timetable_change.action == Action.DELETION:

        regex_match = re.search(
            r'(?:(?P<student_group>[a-žA-Ž0-9\.\s]+):{1})?\s*(?P<subject>[a-žA-Ž\s]+)\s*\-{1}\s*(?P<teacher>[a-žA-Ž\s]+)',
            timetable_change.title)
        if regex_match:
            students_group = regex_match.group("student_group")
            subject = regex_match.group("subject")
            teacher = regex_match.group("teacher")
            hod = Timetable.objects.first()
            '''
            orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                student_class=timetable_change.change_class,
                                                student_group=students_group)'''
            return [Substitution(date=date, new_class=None, new_lesson=None,
                                 timetable=hod,
                                 new_subject=None, new_teacher=None)]
        else:
            return []
    else:
        return []


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