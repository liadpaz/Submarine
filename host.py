from socket import socket

from protocol.client import Client
from ui.console_io import ConsoleIO
from ui.game import Game
from ui.board import BoardState

SUB = BoardState.SUBMARINE
UNK = BoardState.UNKNOWN


def main():
    board = [
        [SUB, SUB, SUB, SUB, SUB, UNK, UNK, UNK, UNK, UNK],
        [UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK],
        [SUB, UNK, SUB, SUB, SUB, UNK, UNK, UNK, UNK, UNK],
        [SUB, UNK, UNK, UNK, UNK, UNK, UNK, SUB, UNK, UNK],
        [UNK, UNK, UNK, UNK, UNK, UNK, UNK, SUB, UNK, UNK],
        [UNK, UNK, UNK, UNK, UNK, UNK, UNK, SUB, UNK, UNK],
        [UNK, UNK, UNK, UNK, UNK, UNK, UNK, SUB, UNK, UNK],
        [UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK],
        [UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK, UNK],
        [SUB, SUB, SUB, UNK, UNK, UNK, UNK, UNK, UNK, UNK],
    ]
    s = socket()

    s.bind(('127.0.0.1', 1234))
    s.listen()
    s, _ = s.accept()

    client = Client(s)

    client.wait_for_message()
    client.send_offer_accept()
    client.send_ready()
    client.wait_for_message()

    game = Game(client, board, True, ConsoleIO())

    game.run()


if __name__ == '__main__':
    main()
