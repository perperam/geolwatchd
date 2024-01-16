from time import sleep
from typing import Callable
import logging

from shapely.geometry import Point

from Blacklist import Blacklist
from Simulator import Simulator, Sensor


class Handler:
    # Add a Debouncer time stamp here
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

        '''
        setting_data_is_none
        0: keep_current_state
        1: unblock_everything
        2: block_everything
        '''
        self.setting_no_data = 1

    def coordinate_in_areas(self, gps_coordinate: Point) -> str | None:
        point = Point(gps_coordinate)

        for area_key in self.blacklist_areas.keys():
            if point.within(self.blacklist_areas[area_key]):
                print(f'inside the {area_key} area')
                return area_key
            else:
                return None

    def run(self) -> None:
        while True:
            cord = self.get_cord()
            print(cord)
            if cord is None:
                match self.setting_no_data:
                    case 0:
                        pass
                    case 1:
                        Handler.unblock()
                    case 2:
                        Handler.block()
            else:
                if self.coordinate_in_areas(cord):
                    Handler.block()
                else:
                    Handler.unblock()

    def get_cord(self) -> Point | None:
        sleep(2)

        data = self.data_endpoint()
        if isinstance(data, tuple):
            return Point(self.data_endpoint())
        else:
            return None


# Example usage
if __name__ == "__main__":
    s = Simulator(
        [[1.0, 1.0], [1.5, 1.5], [2.0, 2.0], [2.5, 2.5], [3.0, 3.0], [3.5, 3.5], [4.0, 4.0], [4.5, 4.5], None, [5.0, 5.0], [5.5, 5.5]],
        interval=5
    )

    g = Sensor()

    blacklist = Blacklist("./blacklist.json")
    p = Processor(s.get_geolocation, blacklist)
    p.run()
