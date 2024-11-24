import socket
import argparse
import sys

def listener_server(server_ip: str, server_port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(0)

        while True:
            client_socket, client_addr = server_socket.accept()

            with client_socket:
                from_client = ''

                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    from_client += data.decode('utf8')
                print (f'Received data: {from_client}')


def get_args():
    parser = argparse.ArgumentParser(description='Run a server that listens for data.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()


    try:
        listener_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
