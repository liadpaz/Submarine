from socket import socket

from common.constants import FirstPlayer
from protocol.client import Client
from protocol.constants import MessageType
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

    s.connect(('192.168.77.9', 1239))

    client = Client(s)
    if client.send_offer(FirstPlayer.PLAYER_OFFERING).type == MessageType.OPEN_REFUSE:
        print('The other player had refused to play')
        return

    try:
        client.wait_for_message()
        client.send_ready()

        game = Game(client, board, False, ConsoleIO())

        game.run()
    except:
        client.disconnect()


if __name__ == '__main__':
    main()
