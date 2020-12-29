"""
Name:       constants.py

Purpose:    This file contains the common constants.
"""
from enum import Enum

CLIENT_PORT = 1234


class GameBoard:
    SIZE = 10


class FirstPlayer(Enum):
    PLAYER_OFFERING = 0
    PLAYER_RECEIVING = 1


class GuessAnswer(Enum):
    """
    This enum represents all the possible answer a guess can return.
    """
    MISS = 0
    HIT = 1
    SUNK = 2
    VICTORY = 3


class ErrorType(Enum):
    INVALID_TYPE = 0
    INVALID_OFFER = 1
    INVALID_COORDINATES = 2
    INVALID_ANSWER = 3
