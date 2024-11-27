import socket
import argparse
import sys
from utils import unpack_message
import threading
from utils import unpack_message
import threading

BACKLOG_SIZE = 1
RECV_BUFSIZE = 4096

def read_all_data(socket: socket.socket) -> str:
    """
    Reads the message from the socket and then CLOSES it.
    
    :param socket: The socket from which the data is read.
    :type socket.socket:
    :returns: The data as an 'utf-8' string.
    :rtype: str
    """
    from_client = b''
    
    with socket:
        while True:
            data = socket.recv(4096)
            if not data:
                break

            from_client += data

    return unpack_message(from_client)


def listener_thread(
        print_lock: threading.Lock,
        client_socket: socket.socket
        ) -> None:
    """
    Reads the message from a socket (until the connection is closed)
    and syncronuously prints it to the screen.

    :param print_lock: The lock that is used for syncronizing the prints between other threads.
    :type threading.Lock:
    :param client_socket: The socket from which the data is read.
    :type socket.socket:

    """
    msg = read_all_data(client_socket)

    with print_lock:
        print (f'Received message: {msg}')


def init_server_socket(server_ip: str, server_port: int) -> None:
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
    server_socket.listen(BACKLOG_SIZE) # This is how many queued connections do we support.

    return server_socket

def run_listener_server(server_ip: str, server_port: int) -> None:
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

    with init_server_socket(server_ip, server_port) as server_socket:

        while True:
            client_socket, client_addr = server_socket.accept()
            
            threading.Thread(target=listener_thread, kwargs={"print_lock":print_lock, "client_socket":client_socket}).start()

    
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
    parser = argparse.ArgumentParser(description='Run a server that listens for data.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main() -> None:
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()


    try:
        run_listener_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
