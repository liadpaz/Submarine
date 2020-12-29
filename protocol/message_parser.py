"""
Name:       message_parser.py

Purpose:    This file contains the method to parse bytes data to a message.
"""
import struct
from struct import unpack

from protocol.constants import MessageType, GuessAnswer, FirstPlayer, ErrorType
from protocol.exceptions import ParseException
from protocol.message import Message
from protocol.messages import MessageOffer, MessageAcceptOffer, MessageRefuseOffer, MessageReady, MessageGuess, \
    MessageGuessAnswer, MessageError, MessageDisconnect


def __parse_offer(data: bytes) -> Message:
    try:
        _, first_player = unpack('<BB', data)
        return MessageOffer(FirstPlayer(first_player))
    except struct.error:
        raise ParseException(ErrorType.INVALID_OFFER)


def __parse_accept(data: bytes) -> Message:
    return MessageAcceptOffer()


def __parse_refuse(data: bytes) -> Message:
    return MessageRefuseOffer()


def __parse_ready(data: bytes) -> Message:
    return MessageReady()


def __parse_guess(data: bytes) -> Message:
    try:
        _, x, y = unpack('<BBB', data)
        return MessageGuess(x, y)
    except struct.error:
        raise ParseException(ErrorType.INVALID_COORDINATES)


def __parse_guess_answer(data: bytes) -> Message:
    try:
        _, answer = unpack('<BB', data)
        return MessageGuessAnswer(GuessAnswer(answer))
    except struct.error:
        raise ParseException(ErrorType.INVALID_ANSWER)


def __parse_disconnect(data: bytes) -> Message:
    return MessageDisconnect()


def __parse_error(data: bytes) -> Message:
    _, error = unpack('<BB', data)
    return MessageError(error)


__parsers__ = {
    MessageType.OPEN_OFFER: __parse_offer,
    MessageType.OPEN_ACCEPT: __parse_accept,
    MessageType.OPEN_REFUSE: __parse_refuse,
    MessageType.OPEN_READY: __parse_ready,
    MessageType.GAME_GUESS: __parse_guess,
    MessageType.GAME_ANSWER: __parse_guess_answer,
    MessageType.GENERAL_DC: __parse_disconnect,
    MessageType.GENERAL_ERROR: __parse_error
}


def parse(data: bytes) -> Message:
    message_type, _ = unpack('<BP', data)
    return __parsers__[message_type](data)
