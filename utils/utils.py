import enum
import json
import logging
from utils.Container import Container
from utils.Shape import Shape

class LoadJsonClassification(enum.Enum):
    INSTANCE = "instance"
    BASE_GEN = "base_gen"

def load_json_from_file(file_path: str) -> tuple[Container, list[Shape]]:
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            shapes_data = json_data['items']
            shapes_list = []
            cont = Container(json_data['container']['x'], json_data['container']['y'], json_data['instance_name'])
            for index, item in enumerate(shapes_data):
                quantity = item['quantity']
                if quantity > 0:
                    for i in range(quantity):
                        shapes_list.append(Shape(item['x'], item['y'], 1, item['value'], f"{index}_{i}"))
                else:
                    logging.debug(f"Shape {item['value']} has quantity 0, skipping")
            return cont, shapes_list

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return None
