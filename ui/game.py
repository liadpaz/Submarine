"""
Name:       ui.py

Purpose:    This file contains the Game class, which represents the ui.
"""
from typing import List, Tuple

from common.constants import GameBoard, GuessAnswer
from ui.base_io import BaseIO
from ui.board import BoardState
from protocol.client import Client


class Game:
    """
    This class represents the game.
    """

    __cell_type_answers__ = {
        BoardState.UNKNOWN: GuessAnswer.MISS,
        BoardState.MISSED: GuessAnswer.MISS,
        BoardState.HIT: GuessAnswer.HIT,
        BoardState.SUNK: GuessAnswer.SUNK,
        BoardState.SUBMARINE: GuessAnswer.HIT,
    }

    def __init__(self, client: Client, board: List[List[BoardState]], this_starting: bool, io: BaseIO):
        """
        :param this_starting: Whether this player is starting the game or not.
        """
        self.client = client
        self.io = io
        self.board = board
        self.enemy_board = [[BoardState.UNKNOWN for _ in range(GameBoard.SIZE)] for _ in range(GameBoard.SIZE)]
        self.this_turn = this_starting
        self.game_over = False

    def run(self):
        """
        This is the main game function. Use this function to play.
        """
        while not self.game_over:
            if self.this_turn:
                x, y = self.__get_coordinates()
                self.__guess(x, y)
            else:
                guess = self.client.wait_for_message()
                guess_answer = self.__board_state(guess.x, guess.y)
                self.client.send_guess_answer(guess_answer)

    def __guess(self, x: int, y: int):
        """
        This method is called when the user guesses a coordinate of the other players submarines.
        """
        self.this_turn = True
        answer = self.client.send_guess(x, y).answer
        if answer == GuessAnswer.MISS:
            self.this_turn = False
            self.enemy_board[x][y] = BoardState.MISSED
        elif answer == GuessAnswer.HIT:
            self.enemy_board[x][y] = BoardState.HIT
        elif answer == GuessAnswer.SUNK:
            self.__sunk_ship(x, y)
        else:
            self.__victory()

    def __handle_guess(self):
        """
        This function handles the other players guess.
        """
        guess = self.client.wait_for_message()
        cell_type = self.board[guess.x, guess.y]
        cell_type = self.__cell_type_answers__[cell_type]
        if cell_type == GuessAnswer.MISS:
            self.this_turn = True
        else:
            if self.__lost():
                cell_type = GuessAnswer.VICTORY
                self.game_over = True
        self.client.send_guess_answer(cell_type)

    def disconnect(self):
        self.client.disconnect()

    def __get_coordinates(self) -> Tuple[int, int]:
        """
        This method gets coordinates from the user.
        """
        valid_input = False
        while not valid_input:
            try:
                x = int(self.io.get_prompted_data("Enter x coordinate: "))
                y = int(self.io.get_prompted_data("Enter y coordinate: "))
                valid_input = True
            except TypeError:
                pass
        return x, y

    def __lost(self) -> bool:
        """
        :return: True if all the submarines had been sunken.
        """
        for row in self.board:
            for cell in row:
                if cell == BoardState.SUBMARINE:
                    return False
        self.io.send_data('You lost!')
        return True

    def __victory(self):
        """
        This method is used to indicate the user has won.
        """
        self.game_over = True
        self.io.send_data('You won!')
        self.client.close()

    def __sunk_ship(self, x: int, y: int):
        """
        This method marks the submarine that contains the specified coordinate as sunken.
        """
        # TODO: mark the coordinates as sunken

    def __board_state(self, x: int, y: int) -> GuessAnswer:
        """
        This method returns the state of the board at the specified cell.
        """
        cell_state = self.board[x][y]
        if cell_state == BoardState.UNKNOWN:
            return GuessAnswer.MISS
        # TODO: find
        return GuessAnswer.HIT
