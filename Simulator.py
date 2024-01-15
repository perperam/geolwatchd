from abc import ABC, abstractmethod
import time


class DataEndpoint(ABC):
    @abstractmethod
    def get_geolocation(self):
        return


class Simulator(DataEndpoint):
    def __init__(self, items, interval=1):
        self.items = items
        self.interval = interval
        self.start_time = time.time()

    def get_geolocation(self) -> list:
        if not self.items:
            raise ValueError("No items in the storage.")

        elapsed_time = time.time() - self.start_time
        index = int(elapsed_time / self.interval) % len(self.items)
        return self.items[index]

    def add_geolocation(self, item) -> None:
        self.items.append(item)

    def reset_storage(self) -> None:
        self.start_time = time.time()


if __name__ == "__main__":
    s = Simulator([[1, 1], [2, 2], [3, 3], [4, 4]], interval=5)
    while True:
        print(s.get_geolocation())
        time.sleep(2)
