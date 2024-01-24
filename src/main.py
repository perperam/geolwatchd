from time import sleep
import logging

from shapely.geometry import Point

from blacklist import Blacklist
from sensor import Sensor
from subscriber import Subscriber


logging.basicConfig(
    filename='info.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Handler:
    def __init__(self):
        # Add a Debouncer time stamp here
        self.is_blocked = False
        self.subscribers = []

    def block(self) -> None:
        if not self.is_blocked:
            self.is_blocked = True

            logging.info("Handler: Blocked")
            print("Handler: Blocked")

            for subscriber in self.subscribers:
                subscriber.notify('BLOCK')

    def unblock(self) -> None:
        if self.is_blocked:
            self.is_blocked = False

            logging.info("Handler: Unblocked")
            print("Handler: Unblocked")

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

        logging.info(f"Processor: blacklist_areas = {self.blacklist_areas}")

    def coordinate_in_areas(self, gps_coordinate: Point) -> str:
        point = Point(gps_coordinate)

        for area_key in self.blacklist_areas.keys():
            if point.within(self.blacklist_areas[area_key]):

                logging.info(f'Processor: inside the {area_key} area')
                print(f'Processor: inside the {area_key} area')

                return area_key
            else:
                return None

    def run(self) -> None:
        while True:
            coord = self.get_cord()

            logging.debug(f'Processor: the Coord is: {coord}')
            print(f'Processor: the Coord is: {coord}')

            if coord is None:
                if self.setting_no_data == 0:
                    pass
                elif self.setting_no_data == 1:
                    self.handler.unblock()
                elif self.setting_no_data == 2:
                    self.handler.block()
            else:
                if self.coordinate_in_areas(coord):
                    self.handler.block()
                else:
                    self.handler.unblock()

    def get_cord(self) -> Point:
        data = self.sensor.get_geolocation()
        if isinstance(data, tuple):
            return Point(self.sensor.get_geolocation())
        else:
            return None
