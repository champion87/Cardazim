import struct
from typing import Union

"""The protocol:
'MSIZE_NBYTES' bytes that describe the length of the message,
followed by the bytes of the message."""

MSIZE_NBYTES = 4
MSIZE_FMT = '<I' # I is for a 4-byte unsigned integer, < i for little endian

def pack_message(message: Union[str, bytes]) -> bytes:
    """
    Packs a message by encoding it to bytes (if necessary) and prepending the message length.
    
    :param message: The message to pack, either as a string or bytes.
    :type message: Union[str, bytes]
    :returns: The packed message as bytes.
    :rtype: bytes
    """
    message_bytes = message.encode('utf-8') if isinstance(message, str) else message
    msg_len = len(message_bytes)
    return struct.pack(MSIZE_FMT, msg_len) + message_bytes

def unpack_message(packed_data: bytes) -> str:
    if len(packed_data) < MSIZE_NBYTES:
        raise Exception("The recieved data is too short to include the bytes for the message size")

    msg_len = struct.unpack(MSIZE_FMT, packed_data[:MSIZE_NBYTES])[0] 
    msg_bytes = packed_data[MSIZE_NBYTES:]

    if len(msg_bytes) != msg_len:
        raise Exception("The recieved message's length differ from the declared length")

    return packed_data[MSIZE_NBYTES:MSIZE_NBYTES + msg_len].decode('utf-8')
