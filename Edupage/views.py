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

from App.logger import logger
from Classroom.classroom_enum import Classroom_filters
from Classroom.equipment_enum import Equipment
from Substitution.models import Substitution
from Timetable.models import Timetable
from Utils.python.result.logic_functions import merge_lessons_records, filter_room_equipment_records, \
    filter_lesson_records, filter_room_records
from Utils.python.result.result_functions import build_results_by_room, build_free_rooms, build_results_by_lesson
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
    # skontroluj ci nie je None napr pre vikend
    if substitutions:
        for sub in substitutions:
            if type(sub.lesson_n) is int:
                sub_lessons.extend(parse_edupage_object(sub, sub.lesson_n, date))
            elif type(sub.lesson_n) is tuple:
                for lesson in range(sub.lesson_n[0], sub.lesson_n[1] + 1):
                    sub_lessons.extend(parse_edupage_object(sub, lesson, date))
    # nezahrn hodiny z rozvrhu, ktore su v dany den v suplovani
    timetable_lessons = Timetable.objects.filter(day=date.strftime("%A")).exclude(
        id__in=map(lambda les: les.timetable_id, sub_lessons))
    return list(chain(timetable_lessons)), list(filter(lambda les: les.new_lesson is not None, sub_lessons))


def parse_edupage_object(timetable_change: TimetableChange, orig_lesson: int, date):
    # skonvertuj triedu zo zaznamov z edupage z rimskych na arabske cisla
    student_class = get_numeric_class(timetable_change.change_class)

    # ak povodna hodina sa presunula alebo nahradila inou
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

            # ak sa presunula hodina do inej ucebne
            if change_room_reg:
                old_room = change_room_reg.group("old_room")
                new_room = change_room_reg.group("new_room")

            # ak povodna hodina odpadla a bola nahradena inou novou hodinou
            # 5. hodina - TV -> nabozenstvo -> za 7.hodinu
            # new_lesson_reg = 7
            if new_lesson_reg:
                moved_lesson = new_lesson_reg.group("moved_lesson")

                # najdi novu hodinu, ktora nahradila odpadnutu
                moved_reg_les = Timetable.objects.filter(lesson=moved_lesson, day=date.strftime("%A"),
                                                         student_class=student_class)
                # ak bola nova hodina v tom case pre danu triedu spolu s inymi hodinami
                # najdi podla skupiny, o ktoru novu hodinu sa jedna
                if len(moved_reg_les) > 1:
                    try:
                        moved_reg_les = moved_reg_les.get(students_group=students_group)
                    except Timetable.DoesNotExist:
                        logger.warning(
                            f'Nenasla sa hodina pre skupinu {students_group} z moznych hodin {[les for les in moved_reg_les]}')
                        return []
                # ak bola nova hodina jedinou hodinou pre celu triedu
                elif len(moved_reg_les) == 1:
                    moved_reg_les = moved_reg_les[0]
                else:
                    logger.warning(
                        f'Nenasla sa nova hodina s parametrami hod:{moved_lesson},{date.strftime("%A")} pre {student_class} '
                        f'z rozvrhu, ktora mala byt presunuta za hodinu v {date}, hod:{orig_lesson} pre {student_class}')
                    return []
                presunuta_hodina = Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                                timetable=moved_reg_les,
                                                new_subject=None, new_teacher=new_teacher)
                # povodna hodina, ktora odpadla alebo sa suplovala
                try:
                    orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                        student_class=student_class,
                                                        student_group=students_group)
                except Timetable.DoesNotExist:
                    logger.warning(
                        f'Nenasla sa povodna hodina s parametrami hod:{orig_lesson},{date.strftime("%A")} pre {student_class} a {students_group}'
                        f'z rozvrhu, ktora mala byt suplovana dna {date}')
                    return []
                odpadnuta_hodina = Substitution(date=date, new_class=None, new_lesson=None, timetable=orig_record,
                                                new_subject=None, new_teacher=None)
                return [presunuta_hodina, odpadnuta_hodina]
            # ak nie je presun za ziadnu hodinu
            # iba sa zmenila dana hodina v dany cas na inu hodinu bez presunu
            else:
                try:
                    orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                        student_class=student_class,
                                                        student_group=students_group)
                except Timetable.DoesNotExist:
                    logger.warning(
                        f'Nenasla sa povodna hodina s parametrami hod:{orig_lesson},{date.strftime("%A")} pre {student_class} a {students_group}'
                        f'z rozvrhu, ktora mala byt suplovana dna {date}')
                    return []

                return [Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                     timetable=orig_record,
                                     new_subject=new_subject, new_teacher=new_teacher)]
    # ak odpadla povodna hodina
    elif timetable_change.action == Action.DELETION:

        regex_match = re.search(
            r'(?:(?P<student_group>[a-žA-Ž0-9\.\s]+):{1})?\s*(?P<subject>[a-žA-Ž\s]+)\s*\-{1}\s*(?P<teacher>[a-žA-Ž\s]+)',
            timetable_change.title)
        if regex_match:
            students_group = regex_match.group("student_group")
            subject = regex_match.group("subject")
            teacher = regex_match.group("teacher")

            try:
                orig_record = Timetable.objects.get(lesson=orig_lesson, day=date.strftime("%A"),
                                                    student_class=student_class,
                                                    student_group=students_group)
            except Timetable.DoesNotExist:
                logger.warning(
                    f'Nenasla sa povodna hodina s parametrami hod:{orig_lesson},{date.strftime("%A")} pre triedu:{student_class} a skupinu:{students_group} '
                    f'z rozvrhu, ktora mala odpadnut dna {date}')
                return []

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
            input_date, input_lesson, input_room_id, equipment_args, parsing_error = parse_inputs(request=request)

            if not parsing_error["is_valid"]:
                return HttpResponse(" ".join(parsing_error["errors"]))

            if not input_date:
                return HttpResponse("Missing date input")

            if input_room_id and len(equipment_args) != 0:
                return HttpResponse("Wrong combination of inputs.")

            if input_date and input_lesson and not input_room_id and len(equipment_args) == 0:
                return search_lesson_view(request, input_date, input_lesson)
            if input_date and input_room_id and not input_lesson:
                return search_room_view(request, input_date, input_room_id)
            if input_date and input_lesson and input_room_id:
                return search_room_lesson_view(request, input_date, input_lesson, input_room_id)
            if input_date and input_lesson and len(equipment_args) != 0:
                return search_filter_rooms_lesson(request, input_date, input_lesson, equipment_args)
            else:
                return HttpResponse("Wrong combination of inputs.")


def parse_inputs(request):
    error_context = {"is_valid": True,
                     "errors": []
                     }
    try:
        input_lesson = int(request.GET.get(Classroom_filters.LESSON.value))
    except ValueError:
        error_context["errors"].append(f'Parameter:{Classroom_filters.LESSON.value} can not be converted into int.')
        error_context["is_valid"] = False
        input_lesson = None
    except TypeError:
        input_lesson = None

    try:
        input_room_id = int(request.GET.get(Classroom_filters.CLASSROOM_ID.value))
    except ValueError:
        error_context["errors"].append(
            f'Parameter:{Classroom_filters.CLASSROOM_ID.value} can not be converted into int.')
        error_context["is_valid"] = False
        input_room_id = None
    except TypeError:
        input_room_id = None

    try:
        str_date = request.GET.get(Classroom_filters.DATE.value)
        input_date = datetime.strptime(str_date, '%Y-%m-%d').date()
    except ValueError:
        error_context["errors"].append(
            f'Parameter:{Classroom_filters.DATE.value} can not be converted into date. It has to be in format YYYY-MM-DD.')
        error_context["is_valid"] = False
        input_date = None
    except TypeError:
        input_date = None

    equipment_args = {}
    for key, value in list(request.GET.items()):
        if key in [eq.value for eq in Equipment]:
            if not (equipment_args[key] == "1" or equipment_args[key] == "0"):
                error_context["errors"].append(
                    f'Parameter:{key} is invalid. Possible option is 0 or 1.')
                error_context["is_valid"] = False
            equipment_args[key] = value == "1"
    return input_date, input_lesson, input_room_id, equipment_args, error_context


def search_room_view(request, date, room_id):
    # search/?date=2023-02-27&classroom=1

    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_room_records(timetable_lessons, sub_lessons, room_id)

    results = merge_lessons_records(timetable_results, sub_results, date)

    return HttpResponse(json.dumps(build_results_by_lesson(results), default=str))


def search_lesson_view(request, date, lesson):
    # search/?date=2023-03-17&lesson=1
    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)

    results = merge_lessons_records(timetable_results, sub_results, date)
    return HttpResponse(json.dumps(build_results_by_room(results), default=str))


def search_room_lesson_view(request, date, lesson, room_id):
    # search/?date=2023-03-17&lesson=1&classroom=1

    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)
    timetable_results, sub_results = filter_room_records(timetable_results, sub_results, room_id)

    results = merge_lessons_records(timetable_results, sub_results, date)
    return HttpResponse((len(results) == 0, json.dumps(results, default=str)))


def search_filter_rooms_lesson(request, date, lesson, equipment_args):
    # search/?date=2023-03-17&lesson=1&teacher_pc=1&data_projector=1
    timetable_lessons, sub_lessons = get_day_records(date)
    timetable_results, sub_results = filter_lesson_records(timetable_lessons, sub_lessons, lesson)
    timetable_results, sub_results = filter_room_equipment_records(timetable_results, sub_results, equipment_args)

    results = merge_lessons_records(timetable_results, sub_results, date)
    context = build_free_rooms(results, equipment_args)
    return HttpResponse(json.dumps(context, default=str))
