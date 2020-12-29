"""
Name:       messages.py

Purpose:    This file contains definitions for all the messages types.
"""
from struct import pack

from common.constants import GameBoard, GuessAnswer, FirstPlayer, ErrorType
from protocol.message import Message
from protocol.constants import MessageType


class MessageOffer(Message):
    """
    This class represents an offer message, in which one player offers another player to play with him.
    """

    def __init__(self, first_player: FirstPlayer):
        """
        :param first_player: assuming each player is represented by his number (0-255)
        """
        self.first_player = first_player

    @property
    def type(self) -> int:
        return MessageType.OPEN_OFFER

    def pack_message(self) -> bytes:
        return pack('<BB', self.type, self.first_player)


class MessageAcceptOffer(Message):
    """
    This class represents the accept offer message.
    """

    @property
    def type(self) -> int:
        return MessageType.OPEN_ACCEPT

    def pack_message(self) -> bytes:
        return pack('<B', self.type)


class MessageRefuseOffer(Message):
    """
    This class represents the refuse offer message.
    """

    @property
    def type(self) -> int:
        return MessageType.OPEN_REFUSE

    def pack_message(self) -> bytes:
        return pack('<B', self.type)


class MessageReady(Message):
    """
    This class represents the ready message.
    """

    @property
    def type(self) -> int:
        return MessageType.OPEN_READY

    def pack_message(self) -> bytes:
        return pack('<B', self.type)


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
        return pack('<BBB', self.type, self.x, self.y)


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
        return pack('<BB', self.type, self.answer)


class MessageDisconnect(Message):
    """
    This class represents a disconnect message in which the player sending this message has disconnected from the game.
    """

    @property
    def type(self) -> int:
        return MessageType.GENERAL_DC

    def pack_message(self) -> bytes:
        return pack('<B', self.type)


class MessageError(Message):
    """
    This class represents a general error message.
    """

    def __init__(self, error: ErrorType):
        self.error = error

    @property
    def type(self) -> int:
        return MessageType.GENERAL_ERROR

    def pack_message(self) -> bytes:
        return pack('<BB', self.type, self.error)
