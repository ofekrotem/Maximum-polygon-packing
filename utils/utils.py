import enum
import json
import logging
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution

class LoadJsonClassification(enum.Enum):
    INSTANCE = "instance"
    BASE_GEN = "base_gen"

def load_json_from_file(file_path: str, classification: LoadJsonClassification) -> (Container, list[Shape]) or list[Solution]:
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            if classification == LoadJsonClassification.INSTANCE:
                shapes_data = json_data['items']
                shapes_list = []
                cont = Container(json_data['container']['x'], json_data['container']['y'], json_data['instance_name'])
                for index, item in enumerate(shapes_data):
                    shapes_list.append(Shape(item['x'], item['y'], item['quantity'], item['value'], index))
                return cont, shapes_list
            elif classification == LoadJsonClassification.BASE_GEN:
                solutions_data = json_data
                solutions_list = []
                for solution_json in solutions_data:
                    solution = Solution.import_from_json(solution_json)
                    solutions_list.append(solution)
                return solutions_list
            else:
                raise Exception("Invalid Classification")

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return None
