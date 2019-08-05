from enum import Enum


class Player(object):
    NOBODY = 0
    PLAYER = 1
    BOT = 2


class Weapons(object):
    NOBODY = 0
    NOTHING = 1
    ROCK = 2
    PAPER = 3
    SCISSORS = 4
    FLAG = 5
    TRAP = 6


class States(Enum):
    MENU = 0
    MAP = 1
    MAP_SHUFFLE = 2
    MAP_PLAY = 3
    MAP_DUEL = 4
    END = 5


class Duel(Enum):
    WIN = 0
    LOSE = 1
    DRAW = 2
    FLAG = 3


class MapSettings(object):
    CANVAS_WIDTH = 950
    CANVAS_HEIGHT = 830
    MAP_COLUMNS = 7
    MAP_ROWS = 6
    MAP_LEFT_EDGE_X = 419.5
    MAP_RIGHT_EDGE_X = 832.5
    MAP_TOP_EDGE_Y = 235.5
    MAP_BOTTOM_EDGE_Y = 589.5
    MAP_FIELD_A = 59
