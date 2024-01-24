from abc import ABC, abstractmethod
import time

import pynmea2
import serial


class Sensor(ABC):
    @abstractmethod
    def get_geolocation(self) -> tuple | None:
        pass


class Simulator(Sensor):
    def __init__(self, items, interval=1):
        self.items = items
        self.interval = interval
        self.start_time = time.time()

    def get_geolocation(self) -> tuple | None:
        if not self.items:
            raise ValueError("No items in the storage.")

        elapsed_time = time.time() - self.start_time
        index = int(elapsed_time / self.interval) % len(self.items)

        if self.items[index] is None:
            return None
        else:
            return tuple(self.items[index])

    def add_geolocation(self, item) -> None:
        self.items.append(item)

    def reset_storage(self) -> None:
        self.start_time = time.time()


class GPS(Sensor):
    def __init__(self):
        self.port = "/dev/ttyACM0"
        self.baud_rate = 9600

    def get_geolocation(self) -> tuple | None:
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            line = ser.readline().decode("utf-8").strip()

            # Check if the line is a valid NMEA sentence
            if line.startswith('$'):
                try:
                    msg = pynmea2.parse(line)

                    if isinstance(msg, pynmea2.GGA):
                        print(f"Lat: {msg.latitude} {msg.lat_dir} | "
                              f"Lon: {msg.longitude} {msg.lon_dir} | "
                              f"Alt: {msg.altitude} | "
                              f"NumSats: {msg.num_sats}")

                        if msg.is_valid:
                            return msg.latitude, msg.longitude
                        else:
                            return None

                except pynmea2.ParseError:
                    print(f"Error parsing NMEA sentence: {line}")
                    return None


if __name__ == "__main__":
    # endpoint = Simulator([[1, 1], [2, 2], [3, 3], [4, 4]], interval=5)
    endpoint = Sensor()
    while True:
        print(endpoint.get_geolocation())
        time.sleep(2)
