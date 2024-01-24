import logging

from shapely.geometry import Polygon
import json


class Blacklist:
    def __init__(self, path):
        self.data = None
        self.load_from_file(path)

    def load_from_file(self, path: str) -> None:
        json_file_path = path
        loaded_data = None

        try:
            with open(json_file_path, 'r') as file:
                loaded_data = json.load(file)
        except Exception as e:
            logging.warning(f'Blacklist: {e}')
            print(f'Blacklist: {e}')

        if self.is_valid_json(loaded_data):
            self.data = loaded_data
        else:
            self.data = {}
            logging.warning("Blacklist: blacklist.json is in the wrong format")
            print(Exception("Blacklist: blacklist.json is in the wrong format"))

    def is_valid_json(self, data: dict) -> bool:
        if not isinstance(data, dict):
            return False

        for entry_name, coordinates in data.items():
            if not isinstance(entry_name, str) or not isinstance(coordinates, list):
                return False

            for coord_entry in coordinates:
                if not isinstance(coord_entry, list) or len(coord_entry) != 2 or not all(
                        isinstance(coord, (int, float)) for coord in coord_entry):
                    return False

        return True

    def get_areas(self) -> dict:
        if self.data:
            return {name: Polygon(points) for name, points in zip(self.data.keys(), self.data.values())}
        else:
            return {}


if __name__ == "__main__":
    b = Blacklist("blacklist.json")
    print(b.data)
