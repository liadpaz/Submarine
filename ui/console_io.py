"""
Name:       console_io.py

Purpose:    This file contains the ConsoleIO class, which gets and sends info to/from the user via the console.
"""
from ui.base_io import BaseIO


class ConsoleIO(BaseIO):
    def get_data(self) -> str:
        return input()

    def send_data(self, data: str):
        print(data)

    def get_prompted_data(self, prompt: str) -> str:
        return input(prompt)
