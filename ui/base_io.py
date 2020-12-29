"""
Name:       base_io.py

Purpose:    This file contains the BaseIO interface, which gets and sends info from/to the user.
"""
from abc import ABCMeta, abstractmethod


class BaseIO(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self) -> str:
        """
        :return: A string from the user.
        """

    @abstractmethod
    def send_data(self, data: str):
        """
        :param data: Data to send to the user.
        """

    @abstractmethod
    def get_prompted_data(self, prompt: str) -> str:
        """
        Like get_data but prompts the user before.

        :param prompt: The prompt to the user.
        :return: Like get_data.
        """
