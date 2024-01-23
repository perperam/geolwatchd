import socket


class Subscriber:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def notify(self, message) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))

            try:
                sock.send(message.encode('utf-8'))

            except Exception as e:
                print(e)


if __name__ == '__main__':
    subscriber = Subscriber('localhost', 12345)
    subscriber.notify('HELLO, TCP')