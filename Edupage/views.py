import json
import re
from datetime import datetime
from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException
from edupage_api.substitution import Action, TimetableChange
from urllib3.exceptions import ReadTimeoutError

from Classroom.classroom_enum import Classroom_filters
from Classroom.equipment_enum import Equipment
from Substitution.models import Substitution
from Timetable.models import Timetable
from Utils.python.result.logic_functions import merge_lessons_records, filter_room_equipment_records, \
    filter_lesson_records, filter_room_records
from Utils.python.result.result_functions import build_results_by_room, build_free_rooms, build_results_by_lesson, \
    build_free_room_by_lessons
from Utils.python.utils import get_numeric_class

edupage = Edupage()
try:
    edupage.login("JanImrich", "B6TQBWKKTW", subdomain="gta")
except BadCredentialsException:
    print("Wrong username or password!")
except ReadTimeoutError:
    print("Poor or no connection to internet!")


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
    student_class = get_numeric_class(timetable_change.change_class)
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

                moved_reg_les = Timetable.objects.filter(lesson=moved_lesson, day=date.strftime("%A"),
                                                         student_class=student_class)
                if len(moved_reg_les) > 1:
                    moved_reg_les = moved_reg_les.get(students_group=students_group)
                else:
                    moved_reg_les = moved_reg_les[0]
                presunuta_hodina = Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                                timetable=moved_reg_les,
                                                new_subject=None, new_teacher=new_teacher)
                orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                    student_class=student_class,
                                                    student_group=students_group)
                odpadnuta_hodina = Substitution(date=date, new_class=None, new_lesson=None, timetable=orig_record,
                                                new_subject=None, new_teacher=None)
                return [presunuta_hodina, odpadnuta_hodina]
            else:

                orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                    student_class=student_class,
                                                    student_group=students_group)
                return [Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                     timetable=orig_record,
                                     new_subject=new_subject, new_teacher=new_teacher)]
    elif timetable_change.action == Action.DELETION:

        regex_match = re.search(
            r'(?:(?P<student_group>[a-žA-Ž0-9\.\s]+):{1})?\s*(?P<subject>[a-žA-Ž\s]+)\s*\-{1}\s*(?P<teacher>[a-žA-Ž\s]+)',
            timetable_change.title)
        if regex_match:
            students_group = regex_match.group("student_group")
            subject = regex_match.group("subject")
            teacher = regex_match.group("teacher")

            orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                student_class=student_class,
                                                student_group=students_group)
            return [Substitution(date=date, new_class=None, new_lesson=None,
                                 timetable=orig_record,
                                 new_subject=None, new_teacher=None)]
        else:
            return []
    else:
        return []


class SearchView(View):
    def get(self, request, *args, **kwargs):
        # user get without results
        if (len(list(request.GET.items()))) == 0:
            return render(request, "search_form.html", {})
        else:
            input_date = request.GET.get(Classroom_filters.DATE.value)
            input_room_id = request.GET.get(Classroom_filters.CLASSROOM_ID.value)
            input_lesson = request.GET.get(Classroom_filters.LESSON.value)
            equipment_args = {}
            for key, value in list(request.GET.items()):
                if key in [eq.value for eq in Equipment]:
                    equipment_args[key] = value == "1"

            if not input_date:
                return HttpResponse("Missing date input")

            if input_room_id and len(equipment_args) != 0:
                return HttpResponse("Wrong combination of inputs.")

            if input_date and input_lesson and not input_room_id and len(equipment_args) == 0:
                return search_lesson_view(request)
            if input_date and input_room_id and not input_lesson:
                return search_room_view(request)
            if input_date and input_lesson and input_room_id:
                return search_room_lesson_view(request)
            if input_date and input_lesson and len(equipment_args) != 0:
                return search_filter_rooms_lesson(request)
            else:
                return HttpResponse("Wrong combination of inputs.")


def search_room_view(request):
    # search/?date=2023-02-27&classroom=1
    str_date = request.GET.get(Classroom_filters.DATE.value)
    date = datetime.strptime(str_date, '%Y-%m-%d').date()
    room_id = int(request.GET.get(Classroom_filters.CLASSROOM_ID.value))

    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_room_records(timetable_lessons, sub_lessons, room_id)

    results = merge_lessons_records(timetable_results, sub_results, date)

    return HttpResponse(json.dumps(build_results_by_lesson(results), default=str))


def search_lesson_view(request):
    # search/?date=2023-03-17&lesson=1
    str_date = request.GET.get(Classroom_filters.DATE.value)
    date = datetime.strptime(str_date, '%Y-%m-%d').date()
    lesson = int(request.GET.get(Classroom_filters.LESSON.value))

    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)

    results = merge_lessons_records(timetable_results, sub_results, date)
    return HttpResponse(json.dumps(build_results_by_room(results), default=str))


def search_room_lesson_view(request):
    # search/?date=2023-03-17&lesson=1&classroom=1
    str_date = request.GET.get(Classroom_filters.DATE.value)
    date = datetime.strptime(str_date, '%Y-%m-%d').date()
    lesson = int(request.GET.get(Classroom_filters.LESSON.value))
    room_id = int(request.GET.get(Classroom_filters.CLASSROOM_ID.value))

    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)
    timetable_results, sub_results = filter_room_records(timetable_results, sub_results, room_id)

    results = merge_lessons_records(timetable_results, sub_results, date)
    return HttpResponse((len(results) == 0, json.dumps(results, default=str)))


def search_filter_rooms(request):
    # search/fitted_classrooms/?date=2023-03-17&teacher_pc=1&data_projector=1
    str_date = request.GET.get(Classroom_filters.DATE.value)
    date = datetime.strptime(str_date, '%Y-%m-%d').date()
    equipment_args = {}
    for key, value in list(request.GET.items()):
        if key in [eq.value for eq in Equipment]:
            equipment_args[key] = value == "1"

    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_room_equipment_records(timetable_lessons, sub_lessons, equipment_args)

    results = merge_lessons_records(timetable_results, sub_results, date)
    return HttpResponse(json.dumps(build_free_room_by_lessons(results, equipment_args), default=str))


def search_filter_rooms_lesson(request):
    # search/?date=2023-03-17&lesson=1&teacher_pc=1&data_projector=1
    str_date = request.GET.get(Classroom_filters.DATE.value)
    lesson = int(request.GET.get(Classroom_filters.LESSON.value))
    date = datetime.strptime(str_date, '%Y-%m-%d').date()
    equipment_args = {}
    for key, value in list(request.GET.items()):
        if key in [eq.value for eq in Equipment]:
            equipment_args[key] = value == "1"

    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)
    timetable_results, sub_results = filter_room_equipment_records(timetable_results, sub_results, equipment_args)

    results = merge_lessons_records(timetable_results, sub_results, date)
    context = build_free_rooms(results, equipment_args)
    return HttpResponse(json.dumps(context, default=str))
