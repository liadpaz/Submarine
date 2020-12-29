"""
Name:       board.py

Purpose:    This file contains the BoardState enum which represents every board cell state.
"""
from enum import Enum


class BoardState(Enum):
    UNKNOWN = 0  # the initial state
    MISSED = 1  # a player tried to hit and missed
    HIT = 2  # a player tried to hit and missed
    SUNK = 3  # a submarine had sunken
    SUBMARINE = 4  # a submarine
