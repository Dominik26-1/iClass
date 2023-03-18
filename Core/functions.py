from datetime import datetime
from itertools import chain

from django.db.models import Q
from edupage_api import TimetableChange

from Classroom.classroom_enum import Classroom_filters
from Classroom.equipment_enum import Equipment
from Core.filter_functions import filter_lesson_records, merge_lessons_records, filter_room_records
from Edupage.access import edupage
from Edupage.functions import parse_edupage_object
from Reservation.models import Reservation
from Substitution.models import Substitution
from Timetable.models import Timetable


def get_day_records(date) -> (list[Timetable], list[Substitution], list[Reservation]):
    reservations = Reservation.objects.filter(date=date)

    substitutions: list[TimetableChange] = edupage.get_timetable_changes(date)
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
    timetable_lessons = Timetable.objects.filter(Q(day=date.strftime("%A")) & Q(valid_from__lte=date) &
                                                 (Q(valid_to__gte=date) | Q(valid_to__isnull=True))).exclude(
        id__in=map(lambda les: les.timetable_id, sub_lessons))
    return list(chain(timetable_lessons)), \
           list(filter(lambda les: les.new_lesson is not None, sub_lessons)), list(chain(reservations))


def is_classroom_available(date, lesson, room_id):
    # search/?date=2023-03-17&lesson=1&classroom=1
    timetable_lessons, sub_lessons, reservation_lessons = get_day_records(date)
    timetable_results, sub_results, reservation_lessons = filter_lesson_records(timetable_lessons, sub_lessons,
                                                                                reservation_lessons, lesson)
    timetable_results, sub_results, reservation_lessons = filter_room_records(timetable_results, sub_results,
                                                                              reservation_lessons, room_id)

    results = merge_lessons_records(timetable_results, sub_results, reservation_lessons, date)
    return len(results) == 0


def parse_inputs(REST_method):
    error_context = {"is_valid": True,
                     "errors": []
                     }
    try:
        input_lesson = int(REST_method.get(Classroom_filters.LESSON.value))
    except ValueError:
        error_context["errors"].append(f'Parameter:{Classroom_filters.LESSON.value} can not be converted into int.')
        error_context["is_valid"] = False
        input_lesson = None
    except TypeError:
        input_lesson = None

    try:
        input_room_id = int(REST_method.get(Classroom_filters.CLASSROOM_ID.value))
    except ValueError:
        error_context["errors"].append(
            f'Parameter:{Classroom_filters.CLASSROOM_ID.value} can not be converted into int.')
        error_context["is_valid"] = False
        input_room_id = None
    except TypeError:
        input_room_id = None

    try:
        str_date = REST_method.get(Classroom_filters.DATE.value)
        input_date = datetime.strptime(str_date, '%Y-%m-%d').date()
    except ValueError:
        error_context["errors"].append(
            f'Parameter:{Classroom_filters.DATE.value} can not be converted into date. It has to be in format YYYY-MM-DD.')
        error_context["is_valid"] = False
        input_date = None
    except TypeError:
        input_date = None

    equipment_args = {}
    for key, value in list(REST_method.items()):
        if key in [eq.value for eq in Equipment]:
            if not (value == "1" or value == "0"):
                error_context["errors"].append(
                    f'Parameter:{key} is invalid. Possible option is 0 or 1.')
                error_context["is_valid"] = False
            equipment_args[key] = value == "1"
    return input_date, input_lesson, input_room_id, equipment_args, error_context
