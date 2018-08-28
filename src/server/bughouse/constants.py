from enum import Enum


class PlayerResult(Enum):
    WIN = 0
    LOSS = 1
    DRAW = 2


class BoardCode(Enum):
    BOARD_A = "board_a"
    BOARD_B = "board_b"


class GameResult(Enum):
    WHITE_WIN = 0
    BLACK_WIN = 1
    DRAW = 2


class PositionCode(Enum):
    WHITE_A = "white_a"
    BLACK_A = "black_a"
    WHITE_B = "white_b"
    BLACK_B = "black_b"
