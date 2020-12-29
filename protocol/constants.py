"""
Name:       constants.py

Purpose:    This file contains constants for the protocol client.
"""

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
