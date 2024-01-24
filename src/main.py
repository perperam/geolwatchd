from time import sleep

from shapely.geometry import Point

from blacklist import Blacklist
from sensor import Sensor
from subscriber import Subscriber


class Handler:
    def __init__(self):
        # Add a Debouncer time stamp here
        self.is_blocked = False
        self.subscribers = []

    def block(self) -> None:
        if not self.is_blocked:
            self.is_blocked = True
            print("Blocked")
            for subscriber in self.subscribers:
                subscriber.notify('BLOCK')

    def unblock(self) -> None:
        if self.is_blocked:
            self.is_blocked = False
            print("Unblocked")
            for subscriber in self.subscribers:
                subscriber.notify('UNBLOCK')

    def add_subscriber(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)
        if self.is_blocked:
            subscriber.notify('BLOCK')


class Processor:
    def __init__(self, sensor: Sensor, blacklist: Blacklist, handler: Handler):
        self.sensor = sensor
        self.blacklist_areas = blacklist.get_areas()
        self.handler = handler

        '''
        setting_data_is_none
        0: keep_current_state
        1: unblock_everything
        2: block_everything
        '''
        self.setting_no_data = 1
        self.within_areas = []

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
                        self.handler.unblock()
                    case 2:
                        self.handler.block()
            else:
                if self.coordinate_in_areas(cord):
                    self.handler.block()
                else:
                    self.handler.unblock()

    def get_cord(self) -> Point | None:
        sleep(2)

        data = self.sensor.get_geolocation()
        if isinstance(data, tuple):
            return Point(self.sensor.get_geolocation())
        else:
            return None
