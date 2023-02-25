from enum import Enum


class Classroom_attributes(Enum):
    LESSON = "lesson"
    DATE = "date"
    CLASSROOM_ID = "classroom"
    WEEKDAY = "weekday"
    STRING_DATE = "date_str"
    EQUIPMENT = [""]


class Equipment(Enum):
    PC = "teacher_pc"
    INTERACTIVE_BOARD = "interactive_board"
    NOTEBOOK = "teacher_notebook"
    FLIP_CHART = "flip_chart"
    SINK = "sink"
    DATA_PROJECTOR = "data_projector"
    ETHERNET_CABLE = "ethernet_cable"