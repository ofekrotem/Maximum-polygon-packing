import copy
import logging
from utils.Solution import Solution
from utils.Shape import Shape
from utils.Container import Container
from enum import Enum
import random
from shapely.geometry import Polygon

random.seed(0)

# Consts
TYPE = "cgshop2024_solution"
NAME = "atris42"
META = {"approach": "generated solution"}

class AlgoClassification(Enum):
    RANDOM = "random"
    SORT_BY_AREA = "sort_by_area"
    SORT_BY_VALUE = "sort_by_value"
    SORT_BY_PERIMETER = "sort_by_perimeter"

class Algo:
    def __init__(self, shapes: list[Shape], cont: Container, tries_on_random_creation: int = 100):
        self.Shapes = shapes
        self.Container = cont
        self.TriesOnRandomCreation = tries_on_random_creation

    def sort_value(self) -> list[Shape]:
        shapes_copy = copy.deepcopy(self.Shapes)
        return sorted(shapes_copy, key=lambda s: s.Value, reverse=True)

    def sort_area(self) -> list[Shape]:
        shapes_copy = copy.deepcopy(self.Shapes)
        return sorted(shapes_copy, key=lambda s: s.get_area())

    def shuffle_list(self) -> list[Shape]:
        shapes_copy = copy.deepcopy(self.Shapes)
        shuffled = shapes_copy[:]
        random.shuffle(shuffled)
        return shuffled

    def sort_by_perimeter(self) -> list[Shape]:
        shapes_copy = copy.deepcopy(self.Shapes)
        return sorted(shapes_copy, key=lambda s: s.get_perimeter())

    def find_ranges(self, s: Shape) -> tuple[int, int, int, int]:
        min_shape_x = min(s.X_cor)
        max_shape_x = max(s.X_cor)
        min_shape_y = min(s.Y_cor)
        max_shape_y = max(s.Y_cor)

        min_container_x = min(self.Container.X_cor)
        max_container_x = max(self.Container.X_cor)
        min_container_y = min(self.Container.Y_cor)
        max_container_y = max(self.Container.Y_cor)

        min_x = min_container_x - min_shape_x
        max_x = max_container_x - max_shape_x
        min_y = min_container_y - min_shape_y
        max_y = max_container_y - max_shape_y

        return min_x, min_y, max_x, max_y

    def create_random_offset_solution(self, classification: AlgoClassification) -> Solution:
        s = Solution(TYPE, NAME, META, self.Container, [])
        solution_shapes_list = []

        if classification == AlgoClassification.RANDOM:
            logging.debug("Random shapes list")
            solution_shapes_list = self.shuffle_list()
        elif classification == AlgoClassification.SORT_BY_AREA:
            logging.debug("Sorted by area")
            solution_shapes_list = self.sort_area()
        elif classification == AlgoClassification.SORT_BY_VALUE:
            logging.debug("Sorted by value")
            solution_shapes_list = self.sort_value()
        elif classification == AlgoClassification.SORT_BY_PERIMETER:
            logging.debug("Sorted by perimeter")
            solution_shapes_list = self.sort_by_perimeter()

        for shape in solution_shapes_list:
            found_place = False
            min_x, min_y, max_x, max_y = self.find_ranges(shape)
            logging.debug(f"Shape {shape.Index}, Ranges: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y}")

            for i in range(self.TriesOnRandomCreation):
                x_sample = random.randint(min_x, max_x)
                y_sample = random.randint(min_y, max_y)
                logging.debug(f"Trying to place {shape.Index} with Ranges: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y} at ({x_sample}, {y_sample})")
                shape.X_offset = x_sample
                shape.Y_offset = y_sample
                s.Shapes.append(shape)

                ans = s.is_valid()
                if ans:
                    logging.debug(f"Placed shape {shape.Index} successfully at ({x_sample}, {y_sample})")
                    found_place = True
                    break
                else:
                    logging.debug(f"Could not place shape {shape.Index} at ({x_sample}, {y_sample})")
                    shape.X_offset = 0
                    shape.Y_offset = 0
                    s.Shapes.remove(shape)

            if not found_place:
                logging.warning(f"Could not place shape {shape.Index} after {self.TriesOnRandomCreation} tries.")

        logging.debug(s)
        return s

    def create_bottom_left_solution(self,classification: AlgoClassification) -> Solution:
        s = Solution(TYPE, NAME, META, self.Container, [])

        sorted_shapes = []

        if classification == AlgoClassification.RANDOM:
            logging.debug("Random shapes list")
            sorted_shapes = self.shuffle_list()
        elif classification == AlgoClassification.SORT_BY_AREA:
            logging.debug("Sorted by area")
            sorted_shapes = self.sort_area()
        elif classification == AlgoClassification.SORT_BY_VALUE:
            logging.debug("Sorted by value")
            sorted_shapes = self.sort_value()
        elif classification == AlgoClassification.SORT_BY_PERIMETER:
            logging.debug("Sorted by perimeter")
            sorted_shapes = self.sort_by_perimeter()

        logging.info(f"Starting bottom-left placement with {len(sorted_shapes)} shapes.")
        for shape in sorted_shapes:
            x, y = self.find_bottom_left_position(shape,s)
            if x is not None and y is not None:
                logging.info(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                logging.warning(f"Could not place shape {shape.Index}. No valid position found.")

        logging.debug(f"Final Solution: {s}")
        return s

    def find_bottom_left_position(self, shape: Shape,currSolution: Solution) -> tuple[int, int]:
        candidate_positions = [(min(self.Container.X_cor), min(self.Container.Y_cor))]  # Start with the bottom-left corner

        for locatedShape in currSolution.Shapes:
            poly = locatedShape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            print(f"Shape {locatedShape.Index} bounds: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")
            logging.debug(f"Shape {locatedShape.Index} bounds: minx={minx}, miny={miny}")
            candidate_positions.append((maxx+1, miny+1))  # Right of the shape
            candidate_positions.append((minx+1, maxy+1))  # Above the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[1], pos[0]))  # Sort by y, then by x

        for x, y in candidate_positions:
            possible_x_offset = x - min(shape.X_cor)
            possible_y_offset = y - min(shape.Y_cor)
            logging.debug(f"Checking position ({x}, {y}) for shape {shape.Index}.")
            shape.X_offset = possible_x_offset
            shape.Y_offset = possible_y_offset
            currSolution.Shapes.append(shape)
            isValid = currSolution.is_valid()
            if isValid:
                return possible_x_offset, possible_y_offset
            else:
                shape.X_offset = 0
                shape.Y_offset = 0
                currSolution.Shapes.remove(shape)

        return None, None

    def create_shape_polygon(self, shape: Shape, x_offset: int, y_offset: int) -> Polygon:
        vertices = [(x + x_offset, y + y_offset) for x, y in zip(shape.X_cor, shape.Y_cor)]
        return Polygon(vertices)
