from itertools import chain

from django.db.models import F

from Classroom.models import Classroom
from Substitution.models import Substitution
from Timetable.models import Timetable


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
    sub_lessons = Substitution.objects.filter(date=date)
    weekday = date.strftime("%A")
    # nezahrn tie ktore su v suplovani
    timetable_lessons = Timetable.objects.filter(day=weekday) \
        .exclude(id__in=sub_lessons.values_list('timetable_id'))
    return timetable_lessons, sub_lessons.exclude(new_lesson=None)




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