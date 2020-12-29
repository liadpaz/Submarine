"""
Name:       exceptions.py

Purpose:    This file contains the protocol exceptions.
"""
from common.constants import ErrorType
from protocol.messages import MessageError


class ParseException(Exception):
    """
    This exception can occur when a received message has corrupted/invalid data.
    """

    def __init__(self, error: ErrorType):
        super(ParseException, self).__init__()
        self.error = error

    def error_message(self) -> MessageError:
        return MessageError(self.error)
