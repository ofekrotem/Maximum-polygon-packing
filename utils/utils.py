import json
import logging
from utils.Container import Container
from utils.Shape import Shape

def load_json_from_file(file_path: str) -> tuple[Container, list[Shape]]:
    """
    Loads JSON data from a file and parses it into a Container and a list of Shapes.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        tuple[Container, list[Shape]]: A tuple containing the Container and a list of Shapes.

    Raises:
        FileNotFoundError: If the file at the specified path is not found.
        json.JSONDecodeError: If there is an error decoding the JSON data.
    """
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
            return cont, shapes_list

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return None
