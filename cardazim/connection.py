from __future__ import annotations
import socket
from utils import pack_message, unpack_message

RECV_BUFSIZE = 4096

class Connection:
    
    def __init__(self, connection: socket.socket):
        self.connection: socket.socket = connection


    @classmethod
    def connect(cls, host_ip:str, port:int) -> Connection:
        connection : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.connect((host_ip, port))
        return cls(connection)


    def close(self) -> None:
        self.connection.close()


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} from {self.connection.getsockname()} to {self.connection.getpeername()}>"


    def send_message(self, message: bytes):
        """
        Sends a message to the connected peer.
        
        :param message: The message to send.
        :type bytes:
        :raises Exception: If the sending fails.
        """
        self.connection.sendall(pack_message(message))


    def recieve_message(self) -> bytes:
        """
        Receives a message from the connected peer.
        
        :raises Exception: If the connection is closed before the message is fully received.
        :return: the recieved msg.
        :rtype: bytes
        """
        from_client = b""

        while True:
            if not (data := self.connection.recv(RECV_BUFSIZE)):
                break

            from_client += data

        return unpack_message(from_client, decode_result=False)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
