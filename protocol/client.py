"""
Name:       client.py

Purpose:    This file contains the Client class, which represents a protocol client.
"""
from socket import socket as Socket
from protocol.constants import BUFFER_SIZE
from protocol.exceptions import ParseException
from protocol.message import Message
from protocol.message_parser import parse
from protocol.messages import MessageDisconnect


class Client:

    def __init__(self, socket: Socket):
        """
        :param socket: A socket to use. The socket must be already open and connected to the other user.
        """
        self.socket = socket

    def message(self, message: Message) -> Message:
        """
        This method messages the other player and returns a message from him.

        :param message: The message to send to the other player.
        :return: The returned message from the other player.
        """
        self._send_message(message)
        return self._get_message()

    def disconnect(self):
        """
        Use this method to send a disconnect message to the other player.

        Note:   we ignore the possible IOError because we want to disconnect, and if an IOError had occurred it is
                possible that the other player had already been disconnected.
        """
        try:
            self._send_message(MessageDisconnect())
        except IOError:
            pass
        finally:
            self.close()

    def close(self):
        """
        This method closes the socket connection and must be called at the end of the client usage.
        """
        self.socket.close()

    def _get_message(self) -> Message:
        """
        This method gets a message from the other player and handles corrupted/invalid messages by sending an error
         message to the other player and waiting for a valid message.

        :return: A message from the other player.
        """
        valid_message_received = False

        while not valid_message_received:
            try:
                message = parse(self.socket.recv(BUFFER_SIZE))
                valid_message_received = True
            except ParseException as e:
                self._send_message(e.error_message())

        return message

    def _send_message(self, message: Message):
        """
        This method sends a message to the other player.

        :param message: The message to send.
        """
        self.socket.sendall(message.pack_message())
