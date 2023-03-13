from itertools import chain

from Classroom.models import Classroom
from Substitution.models import Substitution
from Timetable.models import Timetable
from Utils.python.result.RecordResult import Result


def merge_lessons_records(regular_lessons: list[Timetable], sub_lessons: list[Substitution], search_date):
    reg_records = []
    sub_records = []
    for lesson in regular_lessons:
        reg_record = Result(
            lesson.teacher,
            lesson.classroom.name,
            lesson.classroom.id,
            lesson.lesson,
            search_date,
            lesson.student_class,
            lesson.subject
        )
        '''reg_record["students"] = lesson.student_class
        reg_record["search_teacher"] = lesson.teacher
        reg_record["class_room"] = lesson.classroom.name
        reg_record["class_room_id"] = lesson.classroom.id
        reg_record["subject_name"] = lesson.subject
        reg_record["school_lesson"] = lesson.lesson
        reg_record["date"] = search_date'''
        reg_records.append(reg_record)

    for lesson in sub_lessons:
        if lesson.new_class:
            class_room = lesson.new_class.name
            class_room_id = lesson.new_class.id
        else:
            class_room = lesson.timetable.classroom.name
            class_room_id = lesson.timetable.classroom.id

        sub_record = Result(
            lesson.new_teacher or lesson.timetable.teacher,
            class_room,
            class_room_id,
            lesson.new_lesson or lesson.timetable.lesson,
            search_date,
            lesson.timetable.student_class,
            lesson.new_subject or lesson.timetable.subject

        )
        sub_records.append(sub_record)
        reg_records.extend(sub_records)
    return reg_records


def get_day_records(date):
    # nezahrn tie hodiny, ktore odpadli
    sub_lessons = Substitution.objects.filter(date=date)
    weekday = date.strftime("%A")
    # nezahrn tie ktore su v suplovani
    timetable_lessons = Timetable.objects.filter(day=weekday) \
        .exclude(id__in=sub_lessons.values_list('timetable_id'))
    return list(chain(timetable_lessons)), list(chain(sub_lessons.exclude(new_lesson=None)))


def filter_lesson_records(timetable_lessons, sub_lessons, lesson):
    return list(filter(lambda l: l.lesson == lesson, timetable_lessons)), list(
        filter(lambda l: l.new_lesson == lesson, sub_lessons))


def filter_room_records(timetable_lessons: list[Timetable], sub_lessons, room_id):
    def filter_room(subtitution: Substitution, orig_room_id):
        if subtitution.new_class:
            return subtitution.new_class.id == orig_room_id
        else:
            return False

    return list(filter(lambda t: t.classroom.id == room_id, timetable_lessons)), list(
        filter(lambda s: filter_room(s, room_id), sub_lessons))


def filter_room_equipment_records(timetable_lessons, sub_lessons, equipment_filters):
    def filter_room(subtitution: Substitution, key, value):
        if subtitution.new_class:
            return getattr(subtitution.new_class, key) == value
        else:
            return False

    for key, value in list(equipment_filters.items()):
        timetable_lessons = list(filter(lambda les: getattr(les.classroom, key) == value, timetable_lessons))
        sub_lessons = list(filter(lambda les: filter_room(les, key, value), sub_lessons))

    return timetable_lessons, sub_lessons


def get_room_candidates_by_filter(equipment_filters):
    filters = {}
    for key, value in list(equipment_filters.items()):
        filters[key] = value
    return list(chain(Classroom.objects.filter(**filters)))
