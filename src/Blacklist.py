from shapely.geometry import Polygon
import json


class Blacklist:
    def __init__(self, path):
        self.data = None
        self.load_from_file(path)

    def load_from_file(self, path: str) -> None:
        json_file_path = path

        try:
            with open(json_file_path, 'r') as file:
                loaded_data = json.load(file)
        except:
            Exception("Could not load Blacklist Config Json")

        if self.is_valid_json(loaded_data):
            self.data = loaded_data
        else:
            Exception("Blacklist data is in the wrong format")

    def is_valid_json(self, data: dict) -> bool:
        if not isinstance(data, dict):
            print("Error 1")
            return False

        for entry_name, coordinates in data.items():
            if not isinstance(entry_name, str) or not isinstance(coordinates, list):
                print("Error 2")
                return False

            for coord_entry in coordinates:
                if not isinstance(coord_entry, list) or len(coord_entry) != 2 or not all(
                        isinstance(coord, (int, float)) for coord in coord_entry):
                    print("Error 3")
                    return False

        return True

    def get_areas(self) -> dict | None:
        if self.data:
            return {name: Polygon(points) for name, points in zip(self.data.keys(), self.data.values())}
        else:
            return None


if __name__ == "__main__":
    b = Blacklist("../blacklist.json")
    print(b.data)
