"""
Name:       constants.py

Purpose:    This file contains constants for the protocol client.
"""
from enum import Enum

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


class State(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2
    GAME_OVER = 3
