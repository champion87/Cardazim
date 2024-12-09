from connection import Connection
import socket


class Listener:
    def __init__(self, host_ip: str, port: int, backlog_size: int = 1000):
        """
        Initializes a Listener object with the specified host IP, port, and backlog size.

        Args:
            host_ip (str): The IP address to bind the listener to.
            port (int): The port number to bind the listener to.
            backlog_size (int, optional): The maximum number of queued connections. Defaults to 1000.
        """
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener_socket.bind((host_ip, port))

        self.listener_socket: socket.socket = listener_socket
        self.backlog_size: int = backlog_size
        self.port: int = port
        self.host_ip: str = host_ip

    def __repr__(self):
        return f"{self.__class__.__name__}(port={self.port}, host=_ip{self.host_ip}, backlog={self.backlog_size})"

    def start(self) -> None:
        """
        Start listening for connections.
        """
        self.listener_socket.listen(self.backlog_size)

    def stop(self) -> None:
        """
        Stops the listener and closes the socket.
        """
        self.listener_socket.close()

    def accept(self) -> Connection:
        """
        Waits for an incoming connection, and accept it as it comes.

        :returns: A 'Connection' object of the accepted connection.
        :rtype: Connection
        """
        connection_socket, _ = self.listener_socket.accept()
        return Connection(connection_socket)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
