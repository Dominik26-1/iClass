from itertools import chain

from Classroom.models import Classroom
from Reservation.models import Reservation
from Substitution.models import Substitution
from Timetable.models import Timetable
from Utils.python.result.RecordResult import Result


def merge_lessons_records(regular_lessons: list[Timetable], sub_lessons: list[Substitution],
                          reserve_lessons: list[Reservation], search_date):
    reg_records = []
    sub_records = []
    reserve_records = []
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
        reg_records.append(reg_record)
    for lesson in reserve_lessons:
        res_record = Result(
            lesson.teacher,
            lesson.classroom.name,
            lesson.classroom.id,
            lesson.lesson,
            search_date
        )
        reserve_records.append(res_record)

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
    reg_records.extend(reserve_records)
    return reg_records


def filter_lesson_records(timetable_lessons, sub_lessons, reservation_lesson, lesson):
    return list(filter(lambda l: l.lesson == lesson, timetable_lessons)), list(
        filter(lambda l: l.new_lesson == lesson, sub_lessons)), \
           list(filter(lambda l: l.lesson == lesson, reservation_lesson))


def filter_room_records(timetable_lessons: list[Timetable], sub_lessons, reservation_lessons, room_id):
    def filter_room(subtitution: Substitution, orig_room_id):
        if subtitution.new_class:
            return subtitution.new_class.id == orig_room_id
        else:
            return False

    return list(filter(lambda t: t.classroom.id == room_id, timetable_lessons)), list(
        filter(lambda s: filter_room(s, room_id), sub_lessons)), list(
        filter(lambda r: r.classroom.id == room_id, reservation_lessons))


def filter_room_equipment_records(timetable_lessons, sub_lessons, reservation_lessons, equipment_filters):
    def filter_room(subtitution: Substitution, key, value):
        if subtitution.new_class:
            return getattr(subtitution.new_class, key) == value
        else:
            return False

    for key, value in list(equipment_filters.items()):
        timetable_lessons = list(filter(lambda les: getattr(les.classroom, key) == value, timetable_lessons))
        sub_lessons = list(filter(lambda les: filter_room(les, key, value), sub_lessons))
        reservation_lessons = list(filter(lambda les: getattr(les.classroom, key) == value, reservation_lessons))

    return timetable_lessons, sub_lessons, reservation_lessons

