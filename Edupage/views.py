import re
from datetime import datetime

from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException
from edupage_api.substitution import Action, TimetableChange
from rest_framework.response import Response
from rest_framework.views import APIView

from Classroom.classroom_enum import Classroom_filters
from Substitution.models import Substitution
from Timetable.models import Timetable
from Utils.python.result.logic_functions import merge_lessons_records
from Utils.python.result.result_functions import build_results_by_room

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
    timetable_lessons = Timetable.objects.filter(day=date.strftime("%A")) \
        .exclude(id__in=sub_lessons.values_list('timetable_id'))
    return timetable_lessons, sub_lessons.exclude(new_lesson=None)


def parse_edupage_object(timetable_change: TimetableChange, orig_lesson, date):
    if timetable_change.action == Action.CHANGE:
        regex_match = re.search(
            r'^(?:(?P<student_group>[a-žA-Ž0-9\.\s]+):{1})?(?:\s*\({1}(?P<old_subject>[a-žA-Ž\s]+)\){1}\s*➔{1}\s*)?\s*(?P<new_subject>[a-žA-Ž\s]+)\s+\-{1}\s*(Suplovanie{1}):{1}\s*\({1}(?P<old_teacher>[A-Ža-ž\s]+)[\s)]+➔{1}\s*(?P<new_teacher>[[A-Ža-ž\s]+)',
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
                moved_reg_les = Timetable.objects.get(lesson=moved_lesson, day=date.strftime("%A"),
                                                      student_class=timetable_change.change_class,
                                                      student_group=students_group)
                presunuta_hodina = Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                                timetable=moved_reg_les,
                                                new_subject=None, new_teacher=new_teacher)
                orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                    student_class=timetable_change.change_class,
                                                    student_group=students_group)
                odpadnuta_hodina = Substitution(date=date, new_class=None, new_lesson=None, timetable=orig_record,
                                                new_subject=None, new_teacher=None)
                return [presunuta_hodina, odpadnuta_hodina]
            else:
                orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                    student_class=timetable_change.change_class,
                                                    student_group=students_group)
                return [Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                     timetable=orig_record,
                                     new_subject=new_subject, new_teacher=new_teacher)]
    elif timetable_change.action == Action.CHANGE:
        return []
    else:
        return []


class EdupageView(APIView):
    #search/edupage/?date = 2023-02-27
    def get(self, request, *args, **kwargs):
        str_date = request.query_params[Classroom_filters.DATE.value]
        date = datetime.strptime(str_date, '%Y-%m-%d').date()
        timetable_lessons, sub_lessons = get_day_records(date)
        results = merge_lessons_records(timetable_lessons, sub_lessons, date)
        return Response(build_results_by_room(results))
