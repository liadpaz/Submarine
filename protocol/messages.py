"""
Name:       messages.py

Purpose:    This file contains definitions for all the messages types.
"""
from struct import pack

from protocol.message import Message
from protocol.constants import MessageType, GameBoard, GuessAnswer

MIN_PLAYER_NUMBER = 0
MAX_PLAYER_NUMBER = 255


class MessageOffer(Message):
    """
    This class represents an offer message, in which one player offers another player to play with him.
    """

    def __init__(self, first_player: int):
        """
        :param first_player: assuming each player is represented by his number (0-255)
        """
        if not MIN_PLAYER_NUMBER <= first_player <= MAX_PLAYER_NUMBER:
            raise ValueError(f'first_player must be a number between {MIN_PLAYER_NUMBER} and {MAX_PLAYER_NUMBER}')
        self.first_player = first_player

    @property
    def type(self) -> int:
        return MessageType.OPEN_OFFER

    def pack_message(self) -> bytes:
        return pack('<cc', self.type, self.first_player)


class MessageGuess(Message):
    """
    This class represents a guess message, in which one player guesses the other submarines position.
    """

    def __init__(self, x: int, y: int):
        if x not in range(GameBoard.SIZE) or y not in range(GameBoard.SIZE):
            raise ValueError(f'x and y coordinates need to be in board range!')
        self.x = x
        self.y = y

    @property
    def type(self) -> int:
        return MessageType.GAME_GUESS

    def pack_message(self) -> bytes:
        return pack('<ccc', self.type, self.x, self.y)


class MessageGuessAnswer(Message):
    """
    This class represents a guess answer message, in which a player answers the other players guess attempt.
    """

    def __init__(self, answer: GuessAnswer):
        self.answer = answer

    @property
    def type(self) -> int:
        return MessageType.GAME_ANSWER

    def pack_message(self) -> bytes:
        return pack('<cc', self.type, self.answer)
