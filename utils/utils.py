import json
import os
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution


def load_json_from_file(file_path: str) -> (Container, list[Shape]):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            shapes_data = json_data['items']
            shapes_list = []
            cont = Container(json_data['container']['x'], json_data['container']['y'], json_data['instance_name'])
            for index, item in enumerate(shapes_data):
                shapes_list.append(Shape(item['x'], item['y'], item['quantity'], item['value'], index))
            return (cont, shapes_list)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
