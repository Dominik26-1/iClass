from dataclasses import dataclass
from datetime import datetime


@dataclass
class Result:
    teacher: str
    class_room: str
    room_id: int
    lesson: int
    date: datetime
    students: str = None
    subject: str = None

