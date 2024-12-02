import argparse
import socket
import sys
import threading

from connection import Connection
from listener import Listener
from utils import init_server_socket, unpack_message


def listener_thread(print_lock: threading.Lock, client_connection: Connection) -> None:
    """
    Reads the message from a Connection (until the connection is closed)
    and syncronuously prints it to the screen.

    :param print_lock: The lock that is used for syncronizing the prints between other threads.
    :type threading.Lock:
    :param client_connection: The connection from which the data is read.
    :type Connection:

    """
    with client_connection:
        msg = client_connection.recieve_message().decode("utf-8")
        with print_lock:
            print(f"Received message: {msg}")


def listener_server(server_ip: str, server_port: int) -> None:
    """
    Opens a server on 'server_ip' at port 'server_port'.
    The server opens a listening thread for each connection
    and prints to the screen every message that it recieves.

    :param server_ip:
    :type str:
    :param server_port:
    :type int:
    """
    print_lock = threading.Lock()

    with Listener(server_ip, server_port) as listener:
        while True:
            conn = listener.accept()
            threading.Thread(
                target=listener_thread,
                kwargs={"print_lock": print_lock, "client_connection": conn},
            ).start()

    # Wait for all threads to finish.
    #
    # this code is unreachable, but if one day I'd want to support quitting while running the server,
    # I would have then to break from the loop and reach this code.
    for thread in threading.enumerate():
        if thread is not threading.main_thread():  # Skip the main thread
            thread.join()


def get_args() -> argparse.Namespace:
    """
    Parse the command line arguments required to run the server.

    :returns: The parsed arguments, as an 'argparse.Namespace' object. Example for usage: 'get_args().server_ip'
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Run a server that listens for data.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()


def main() -> None:
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()

    try:
        listener_server(args.server_ip, args.server_port)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
