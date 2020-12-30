"""
Name:       ui.py

Purpose:    This file contains the Game class, which represents the ui.
"""
from typing import List

from common.constants import GameBoard, GuessAnswer
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

    def __init__(self, client: Client, board: List[List[BoardState]]):
        self.client = client
        self.board = board
        self.enemy_board = [[BoardState.UNKNOWN for _ in range(GameBoard.SIZE)] for _ in range(GameBoard.SIZE)]
        self.this_turn = False
        self.game_over = False

    def run(self):
        """
        This is the main game function. Use this function to play.
        """
        while not self.game_over:
            if self.this_turn:
                pass  # TODO: get input from user and send a guess message

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

    def __lost(self) -> bool:
        """
        :return: True if all the submarines had been sunken.
        """
        for row in self.board:
            for cell in row:
                if cell == BoardState.SUBMARINE:
                    return False
        return True

    def __victory(self):
        """
        This method is used to indicate the user has won.
        """
        self.game_over = True
        # TODO: inform the user that he had won
        self.client.close()

    def __sunk_ship(self, x: int, y: int):
        """
        This method marks the submarine that contains the specified coordinate as sunken.
        """
        # TODO: mark the coordinates as sunken
