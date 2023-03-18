from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from Classroom.models import Classroom
from Core.build_result_function import build_results_by_lesson, build_results_by_room, build_free_rooms
from Core.filter_functions import merge_lessons_records, filter_room_equipment_records, \
    filter_lesson_records, filter_room_records
from Core.functions import get_day_records, parse_inputs
from Utils.python.result.search_result_enum import ResultType


class SearchView(View):
    def get(self, request, *args, **kwargs):
        # user get without results

        if (len(list(request.GET.items()))) == 0:
            content = {
                "classrooms": Classroom.objects.all(),
                "with_results": False
            }
            return render(request, "search_form.html", content)
        else:
            input_date, input_lesson, input_room_id, equipment_args, parsing_error = parse_inputs(
                REST_method=request.GET)

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


def search_room_view(request, date, room_id):
    # search/?date=2023-02-27&classroom=1

    timetable_lessons, sub_lessons, reserved_lessons = get_day_records(date)
    timetable_results, sub_results, reserved_lessons = filter_room_records(timetable_lessons, sub_lessons,
                                                                           reserved_lessons, room_id)

    results = merge_lessons_records(timetable_results, sub_results, reserved_lessons, date)
    all_classrooms = Classroom.objects.all()
    context = {
        "with_results": True,
        "result": build_results_by_lesson(results),
        "result_type": ResultType.LessonList.value,
        "classrooms": all_classrooms,
        "search_params": {
            "date": date,
            "room": room_id,
        },
        "search_room": all_classrooms.get(id=room_id).get_dict()
    }
    return render(request, "search_form.html", context)


def search_lesson_view(request, date, lesson):
    # search/?date=2023-03-17&lesson=1
    timetable_lessons, sub_lessons, reserved_lessons = get_day_records(date)
    timetable_results, sub_results, reserved_lessons = filter_lesson_records(timetable_lessons, sub_lessons,
                                                                             reserved_lessons, lesson)

    results = merge_lessons_records(timetable_results, sub_results, reserved_lessons, date)
    context = {
        "with_results": True,
        "result": build_results_by_room(results),
        "result_type": ResultType.RoomList.value,
        "classrooms": Classroom.objects.all(),
        "search_params": {
            "date": date,
            "lesson": lesson,
        }
    }
    return render(request, "search_form.html", context)


def search_room_lesson_view(request, date, lesson, room_id):
    timetable_lessons, sub_lessons, reserved_lessons = get_day_records(date)
    timetable_results, sub_results, reserved_lessons = filter_lesson_records(timetable_lessons, sub_lessons,
                                                                             reserved_lessons, lesson)
    timetable_results, sub_results, reserved_lessons = filter_room_records(timetable_results, sub_results,
                                                                           reserved_lessons, room_id)

    results = merge_lessons_records(timetable_results, sub_results, reserved_lessons, date)
    context = {
        "with_results": True,
        "result": results,
        "classrooms": Classroom.objects.all(),
        "is_free": len(results) == 0,
        "result_type": ResultType.TrueFalse.value,
        "search_params": {
            "date": date,
            "lesson": lesson,
            "room": room_id,
        },
        "search_room": Classroom.objects.get(id=room_id).get_dict()
    }
    return render(request, "search_form.html", context)


def search_filter_rooms_lesson(request, date, lesson, equipment_args):
    # search/?date=2023-03-17&lesson=1&teacher_pc=1&data_projector=1
    timetable_lessons, sub_lessons, reserved_lessons = get_day_records(date)
    timetable_results, sub_results, reserved_lessons = filter_lesson_records(timetable_lessons, sub_lessons,
                                                                             reserved_lessons, lesson)
    timetable_results, sub_results, reserved_lessons = filter_room_equipment_records(timetable_results, sub_results,
                                                                                     reserved_lessons, equipment_args)

    results = merge_lessons_records(timetable_results, sub_results, reserved_lessons, date)
    context = {
        "with_results": True,
        "result": build_free_rooms(results, equipment_args),
        "result_type": ResultType.RoomList.value,
        "classrooms": Classroom.objects.all(),
        "search_params": {
            "date": date,
            "lesson": lesson,
            "equipment_params": equipment_args,
        }
    }
    return render(request, "search_form.html", context)
