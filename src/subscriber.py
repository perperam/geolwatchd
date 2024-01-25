import socket
import json
import logging


def is_valid_json(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    # this must be extended to do a better testing
    return True


def load_subscribers(path: str) -> list:
    loaded_subscribers = []
    loaded_data = None

    try:
        with open(path, 'r') as file:
            loaded_data = json.load(file)
    except Exception as e:
        logging.warning(f'Subscriber Loader: {e}')
        print(f'Subscriber Loader: {e}')

    if is_valid_json(loaded_data):
        for subs in loaded_data.values():
            loaded_subscribers.append(Subscriber(subs['host'], subs['port']))
        return loaded_subscribers
    else:
        logging.warning("Subscriber Loader: subscribers.json is in the wrong format")
        print(Exception("Subscriber Loader: subscribers.json is in the wrong format"))
        return []


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
