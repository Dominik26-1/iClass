from App.constants import MAX_LESSON
from Classroom.functions import get_room_candidates_by_filter
from Classroom.models import Classroom
from Utils.python.result.RecordResult import Result


def build_results_by_room(results):
    classrooms = Classroom.objects.all()
    room_results = {}
    for room in classrooms:
        room_results[room.id] = {
            "info": room.get_dict(),
            "occupancy": list(filter(lambda less: less.room_id == room.id, results))
        }

    return dict(sorted(room_results.items(), key=lambda room: len(room[1]["occupancy"]) == 0, reverse=True))


def build_results_by_lesson(results: list[Result]):
    room_results = {}
    for lesson in range(MAX_LESSON + 1):
        room_results[lesson] = {"occupancy": list(filter(lambda less: less.lesson == lesson, results))}

    return room_results


def build_free_room_by_lessons(results, filters):
    room_results = {}
    all_matched_rooms = get_room_candidates_by_filter(filters)
    for lesson in range(MAX_LESSON + 1):
        for room in all_matched_rooms:
            if not list(filter(lambda less: (less.lesson == lesson and
                                             less.room_id == room.id), results)):
                room_results[lesson] = {
                    "info": room.get_dict()
                }
    return room_results


def build_free_rooms(results, filters):
    room_results = {}
    all_matched_rooms = get_room_candidates_by_filter(filters)
    for room in all_matched_rooms:
        if not list(filter(lambda less: less.room_id == room.id, results)):
            room_results[room.id] = {
                "info": room.get_dict()
            }
    return room_results
