from enum import Enum


class PlayerResult(Enum):
    WIN = 0
    LOSS = 1
    DRAW = 2


class BoardCode(Enum):
    BOARD_A = "board_a"
    BOARD_B = "board_b"


class GameStatus(Enum):
    WAITING_FOR_PLAYERS = 0
    READY_TO_START = 1
    IN_PROGRESS = 2
    WHITE_WIN = 3
    BLACK_WIN = 4
    DRAW = 5


class PositionCode(Enum):
    WHITE_A = "white_a"
    BLACK_A = "black_a"
    WHITE_B = "white_b"
    BLACK_B = "black_b"
