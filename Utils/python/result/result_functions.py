from Classroom.models import Classroom
from Utils.python.result.logic_functions import get_room_candidates_by_filter

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