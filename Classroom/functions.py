from itertools import chain

from Classroom.models import Classroom


def get_room_candidates_by_filter(equipment_filters):
    filters = {}
    for key, value in list(equipment_filters.items()):
        filters[key] = value
    return list(chain(Classroom.objects.filter(**filters)))
