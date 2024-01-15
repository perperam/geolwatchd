from shapely.geometry import Point
from time import sleep
from typing import Callable

from Blacklist import Blacklist
from Simulator import Simulator


class Handler:
    is_blocked = False

    @staticmethod
    def block() -> None:
        if not Handler.is_blocked:
            Handler.is_blocked = True
            print("Blocked")

    @staticmethod
    def unblock() -> None:
        if Handler.is_blocked:
            Handler.is_blocked = False
            print("Unblocked")


class Processor:
    def __init__(self, data_endpoint: Callable, blacklist: Blacklist):
        self.data_endpoint = data_endpoint
        self.blacklist_areas = blacklist.get_areas()

    def coordinate_in_areas(self, gps_coordinate: Point) -> bool:
        point = Point(gps_coordinate)

        for area in self.blacklist_areas:
            if point.within(area):
                return True
            else:
                return False

    def run(self) -> None:
        while True:
            if self.coordinate_in_areas(self.get_cord()):
                Handler.block()
            else:
                Handler.unblock()

    def get_cord(self) -> Point:
        sleep(2)
        point = Point(self.data_endpoint())
        print(point)
        return point


# Example usage
if __name__ == "__main__":
    s = Simulator(
        [[1, 1], [1.5, 1.5], [2, 2], [2.5, 2.5], [3, 3], [3.5, 3.5], [4, 4], [4.5, 4.5], [5, 5], [5.5, 5.5]],
        interval=5
    )
    b = Blacklist("./blacklist.json")
    p = Processor(s.get_geolocation, b)
    p.run()
