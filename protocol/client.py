"""
Name:       client.py

Purpose:    This file contains the Client class, which represents a protocol client.
"""
from socket import socket as Socket

from common.constants import FirstPlayer, ErrorType, GuessAnswer
from protocol.constants import BUFFER_SIZE, State, MessageType
from protocol.exceptions import ParseException
from protocol.message import Message
from protocol.message_parser import parse
from protocol.messages import MessageDisconnect, MessageGuess, MessageOffer, MessageAcceptOffer, MessageRefuseOffer, \
    MessageReady, MessageGuessAnswer


class Client:

    def __init__(self, socket: Socket):
        """
        :param socket: A socket to use. The socket must be already open and connected to the other user.
        """
        self.socket = socket
        self.__state = State.DISCONNECTED

    def send_offer(self, first_player: FirstPlayer):
        """
        This method sends an offer message to the other player and returns the other player's answer.

        :param first_player: The first player in the game.

        :return: The the other player answer.
        """
        self.__state = State
        answer = self.__message(MessageOffer(first_player))
        if answer.type == MessageType.OPEN_ACCEPT:
            self.__state = State.CONNECTED
        return answer

    def send_offer_accept(self):
        """
        This method sends an accept offer message to the other player.
        """
        self.__state = State.CONNECTED
        return self.__send_message(MessageAcceptOffer())

    def send_offer_refuse(self):
        """
        This method sends a refuse offer message to the other player.
        """
        return self.__send_message(MessageRefuseOffer())

    def send_ready(self):
        """
        This method sends a ready message to the other player.
        """
        self.__state = State.IN_GAME
        self.__send_message(MessageReady())

    def send_guess(self, x: int, y: int) -> MessageGuessAnswer:
        """
        This method sends a guess message to the other player and returns the guess answer.

        :param x: The guess's x coordinate.
        :param y: The guess's y coordinate.

        :return: The guess's answer message from the other player.
        """
        answer = self.__message(MessageGuess(x, y))  # type: MessageGuessAnswer
        if answer.answer == GuessAnswer.VICTORY:
            self.__state = State.GAME_OVER
        return answer

    def send_guess_answer(self, answer: GuessAnswer):
        """
        This method sends a guess answer to the other player.
        """
        if answer == GuessAnswer.VICTORY:
            self.__state = State.GAME_OVER
        self.__send_message(MessageGuessAnswer(answer))

    def wait_for_message(self) -> Message:
        """
        Waits for an incoming message from the other player.
        """
        return self.__get_message()

    def close(self):
        """
        This method closes the socket connection and must be called at the end of the client usage.
        """
        self.socket.close()

    def disconnect(self):
        """
        Use this method to send a disconnect message to the other player.

        Note:   we ignore the possible IOError because we want to disconnect, and if an IOError had occurred it is
                possible that the other player had already been disconnected.
        """
        try:
            self.__send_message(MessageDisconnect())
        except IOError:
            pass
        finally:
            self.close()

    def __message(self, message: Message) -> Message:
        """
        This method sends a message and returns the answer message from the other player.
        """
        self.__send_message(message)
        return self.__get_message()

    def __get_message(self) -> Message:
        """
        This method gets a message from the other player and handles corrupted/invalid messages by sending an error
         message to the other player and waiting for a valid message.

        :return: A message from the other player.
        """
        valid_message_received = False

        while not valid_message_received:
            try:
                message = parse(self.socket.recv(BUFFER_SIZE))
                if self.__check_state(message):
                    valid_message_received = True
                else:
                    raise ParseException(ErrorType.INVALID_TYPE)
            except ParseException as e:
                self.__send_message(e.error_message())

        return message

    def __send_message(self, message: Message):
        """
        This method sends a message to the other player.

        :param message: The message to send.
        """
        self.socket.sendall(message.pack_message())

    def __check_state(self, message: Message) -> bool:
        """
        This method checks the state of the client against the message type.

        :return: True if the type of the message is ok to the client state.
        """
        if message.type in (MessageType.OPEN_ACCEPT, MessageType.OPEN_REFUSE) and self.__state != State.DISCONNECTED:
            return False
        if message.type == MessageType.OPEN_READY and self.__state != State.CONNECTED:
            return False
        if message.type in (MessageType.GAME_GUESS, MessageType.GAME_ANSWER) and self.__state != State.IN_GAME:
            return False
        return True
