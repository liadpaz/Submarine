"""
Name:       constants.py

Purpose:    This file contains constants for the protocol client.
"""
from enum import Enum

CLIENT_PORT = 1234

BUFFER_SIZE = 1024


class MessageType:
    OPEN_OFFER = 100  # offer
    OPEN_ACCEPT = 101  # accept offer
    OPEN_REFUSE = 102  # refuse offer
    OPEN_READY = 103  # all submarines has set & ready to play

    GAME_GUESS = 110  # a guess
    GAME_ANSWER = 111  # answer to a guess

    GENERAL_DC = 50  # disconnect
    GENERAL_ERROR = 99  # error


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
