"""
Name:       constants.py

Purpose:    This file contains constants for the protocol client.
"""
from enum import Enum

CLIENT_PORT = 1234

BUFFER_SIZE = 1024


class MessageType:
    OPEN_OFFER = 100
    OPEN_ACCEPT = 101
    OPEN_REFUSE = 102
    OPEN_START = 103

    GAME_GUESS = 110
    GAME_ANSWER = 111

    GENERAL_DC = 50
    GENERAL_ERROR = 99


class GameBoard:
    SIZE = 10


class GuessAnswer(Enum):
    """
    This enum represents all the possible answer a guess can return.
    """
    MISS = 0
    HIT = 1
    SUNK = 2
    VICTORY = 3
