from Edupage.views import get_day_records
from Utils.python.result.logic_functions import filter_lesson_records, filter_room_records, merge_lessons_records


def is_classroom_available(date, lesson, room_id):
    # search/?date=2023-03-17&lesson=1&classroom=1
    timetable_lessons, sub_lessons, reservation_lessons = get_day_records(date)
    timetable_results, sub_results, reservation_lessons = filter_lesson_records(timetable_lessons, sub_lessons, reservation_lessons, lesson)
    timetable_results, sub_results, reservation_lessons = filter_room_records(timetable_results, sub_results, reservation_lessons, room_id)

    results = merge_lessons_records(timetable_results, sub_results, reservation_lessons, date)
    return len(results) == 0
