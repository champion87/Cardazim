import struct

def pack_message(message: str) -> bytes:
    message_bytes = message.encode('utf-8')
    msg_len = len(message_bytes)
    return struct.pack('<I', msg_len) + message_bytes

def unpack_message(packed_data: bytes) -> str:
    msg_len = struct.unpack('<I', packed_data[:4])[0]
    return packed_data[4:4 + msg_len].decode('utf-8')