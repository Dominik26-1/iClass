from enum import Enum


class Equipment(Enum):
    PC = "teacher_pc", "učiteľský počítač"
    INTERACTIVE_BOARD = "interactive_board", "interaktívna tabuľa"
    NOTEBOOK = "teacher_notebook", "notebook"
    FLIP_CHART = "flip_chart", "flip chart"
    SINK = "sink", "umývadlo"
    DATA_PROJECTOR = "data_projector", "dataprojektor"
    ETHERNET_CABLE = "ethernet_cable", "internatový kábel"
