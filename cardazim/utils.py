import struct
from typing import Union
import socket

"""The protocol:
'MSIZE_NBYTES' bytes that describe the length of the message,
followed by the bytes of the message."""

MSIZE_NBYTES = 4
MSIZE_FMT = "<I"  # I is for a 4-byte unsigned integer, < i for little endian
BACKLOG_SIZE = 1


def pack_message(message: Union[str, bytes]) -> bytes:
    """
    Packs a message by encoding it to bytes (if necessary) and prepending the message length.

    :param message: The message to pack, either as a string or bytes.
    :type message: Union[str, bytes]
    :returns: The packed message as bytes.
    :rtype: bytes
    """
    message_bytes = message.encode("utf-8") if isinstance(message, str) else message
    msg_len = len(message_bytes)
    return struct.pack(MSIZE_FMT, msg_len) + message_bytes


def unpack_message(packed_data: bytes, decode_result: bool = True) -> Union[str, bytes]:
    """
    Unpacks a message from its the data according to the protocol.

    :param packed_data: The message data.
    :type packed_data: bytes
    :param decode_result: If True, the message will be decoded to a string using UTF-8;
                          otherwise, it will be returned as raw bytes.
    :type decode_result: bool
    :return: The unpacked message, either as a string (if `decode_result` is True) or as bytes.
    :rtype: Union[str, bytes]
    :raises Exception: If the data isn't valid according to the protocol.
    """
    if len(packed_data) < MSIZE_NBYTES:
        raise Exception(
            "The recieved data is too short to include the bytes for the message size"
        )

    msg_len = struct.unpack(MSIZE_FMT, packed_data[:MSIZE_NBYTES])[0]
    msg_bytes = packed_data[MSIZE_NBYTES:]

    if len(msg_bytes) != msg_len:
        raise Exception("The recieved message's length differ from the declared length")

    return msg_bytes.decode("utf-8") if decode_result else msg_bytes


def init_server_socket(server_ip: str, server_port: int) -> socket.socket:
    """
    Creates and initializes a socket for the server.

    :param server_ip:
    :type str:
    :param server_port:
    :type int:
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(
        BACKLOG_SIZE
    )  # This is how many queued connections do we support.

    return server_socket
