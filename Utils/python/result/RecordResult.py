from dataclasses import dataclass
from datetime import date


@dataclass
class Result:
    teacher: str
    class_room: str
    room_id: int
    lesson: int
    date: date
    students: str = None
    subject: str = None
