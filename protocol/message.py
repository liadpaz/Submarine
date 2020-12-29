"""
Name:       message.py

Purpose:    This file contains the Message class.
"""
from abc import ABCMeta, abstractmethod


class Message(metaclass=ABCMeta):

    @property
    @abstractmethod
    def type(self) -> int:
        """
        :return: The message type.
        """

    @abstractmethod
    def pack_message(self) -> bytes:
        """
        Use this method to prepare the message for sending as a packet.

        :return: The message as a packet data.
        """
