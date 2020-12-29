"""
Name:       messages.py

Purpose:    This file contains definitions for all the messages types.
"""
from struct import pack

from protocol.message import Message
from protocol.constants import MessageType

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
