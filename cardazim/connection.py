class Connection:
    def __init__(connection: socket.socket):
        pass

    @classmethod
    def connect(cls, host, port):
        pass

    def close(self):
        pass

    def __repr__(self):
        pass

    def send_message(self, message: bytes):
        pass

    def recieve_message(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
