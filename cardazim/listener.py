class Listner:
    def __repr__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def accept(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()