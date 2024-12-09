"""
client.py
This module provides functionality to send card data to a server. It includes
functions to parse command-line arguments, create a card from given data,
serialize it, and send it to a specified server using a connection.
Functions:
    send_data(...)
        Sends serialized card data to the server at the specified IP address and port.
    get_args()
        Parses command-line arguments and returns them.
    main()
        Main function to handle the command-line interface and send data to the server.
"""

import argparse
import sys

from card import Card
from connection import Connection


def send_data(
    server_ip: str,
    server_port: int,
    name: str,
    creator: str,
    image_path: str,
    riddle: str,
    solution: str,
):
    """
    Send data to server in address (server_ip, server_port).
    """
    card = Card.create_from_path(name, creator, image_path, riddle, solution)
    data = card.serialize()
    with Connection.connect(server_ip, server_port) as client:
        client.send_message(data)


def get_args():
    """
    Parses command-line arguments for sending data to the server.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments:
            - server_ip (str): The server's IP address.
            - server_port (int): The server's port number.
            - name (str): The name of the card.
            - creator (str): The creator of the card.
            - image_path (str): The path to the image file.
            - riddle (str): The riddle on the card.
            - solution (str): The solution to the riddle.
    """
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("name", type=str, help="the name of the card")
    parser.add_argument("creator", type=str, help="the creator of the card")
    parser.add_argument("image_path", type=str, help="the path to the image file")
    parser.add_argument("riddle", type=str, help="the riddle on the card")
    parser.add_argument("solution", type=str, help="the solution to the riddle")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_data(
            args.server_ip,
            args.server_port,
            args.name,
            args.creator,
            args.image_path,
            args.riddle,
            args.solution,
        )
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
