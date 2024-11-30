from __future__ import annotations
import socket
from utils import pack_message

class Connection:
    
    def __init__(self, connection: socket.socket):
        self.connection: socket.socket = connection

    @classmethod
    def connect(cls, target_host_ip:str, port:int) -> Connection:
        pass

    def close(self) -> None:
        self.connection.close()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} from {self.connection.getsockname()} to {self.connection.getsockname()}>"

    def send_message(self, message: bytes):
        client.sendall(pack_message(message))

    def recieve_message(self):
        """
        :raises Exception: If the connection was closed before the message was fully recieved
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
