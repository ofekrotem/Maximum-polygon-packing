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

class Algo:
    def __init__(self, shapes: list[Shape], cont: Container, tries_on_random_creation: int = 100):
        self.Shapes = shapes
        self.Container = cont
        self.ShuffledShapes = self.shuffle_list()
        self.SortedbyAreaShapes = self.sort_area()
        self.SortedbyValueShapes = self.sort_value()
        self.TriesOnRandomCreation = tries_on_random_creation

    def sort_value(self) -> list[Shape]:
        return sorted(self.Shapes, key=lambda s: s.Value, reverse=True)

    def sort_area(self) -> list[Shape]:
        return sorted(self.Shapes, key=lambda s: s.get_area())

    def shuffle_list(self) -> list[Shape]:
        shuffled = self.Shapes[:]
        random.shuffle(shuffled)
        return shuffled

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
        s = Solution(TYPE, NAME, META, [], [], [], self.Container, self.Shapes)
        solution_shapes_list = self.Shapes

        if classification == AlgoClassification.RANDOM:
            logging.debug("Random shapes list")
            solution_shapes_list = self.ShuffledShapes
        elif classification == AlgoClassification.SORT_BY_AREA:
            logging.debug("Sorted by area")
            solution_shapes_list = self.SortedbyAreaShapes
        elif classification == AlgoClassification.SORT_BY_VALUE:
            logging.debug("Sorted by value")
            solution_shapes_list = self.SortedbyValueShapes

        for shape in solution_shapes_list:
            min_x, min_y, max_x, max_y = self.find_ranges(shape)
            logging.debug(f"Shape {shape.Index}, Ranges: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y}")

            for i in range(self.TriesOnRandomCreation):
                x_sample = random.randint(min_x, max_x)
                y_sample = random.randint(min_y, max_y)
                logging.debug(f"Trying to place {shape.Index} with Ranges: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y} at ({x_sample}, {y_sample})")
                s.X_Offset.append(x_sample)
                s.Y_Offset.append(y_sample)
                s.Items_ID.append(shape.Index)

                ans = s.is_valid()
                if ans:
                    logging.debug(f"Placed shape {shape.Index} successfully at ({x_sample}, {y_sample})")
                    break
                else:
                    s.X_Offset.pop()
                    s.Y_Offset.pop()
                    s.Items_ID.pop()
        logging.debug(s)
        return s

    def create_bottom_left_solution(self) -> Solution:
        s = Solution(TYPE, NAME, META, [], [], [], self.Container, self.Shapes)
        occupied_spaces = []

        sorted_shapes = self.sort_value()

        logging.info(f"Starting bottom-left placement with {len(sorted_shapes)} shapes.")
        for shape in sorted_shapes:
            x, y = self.find_bottom_left_position(shape, occupied_spaces)
            if x is not None and y is not None:
                s.X_Offset.append(x)
                s.Y_Offset.append(y)
                s.Items_ID.append(shape.Index)
                occupied_spaces.append(self.create_shape_polygon(shape, x, y))
                logging.info(f"Placed shape {shape.Index} at position ({x}, {y}).")
            else:
                logging.warning(f"Could not place shape {shape.Index}. No valid position found.")

        logging.debug(f"Final Solution: {s}")
        return s

    def find_bottom_left_position(self, shape: Shape, occupied_spaces: list[Polygon]) -> tuple[int, int]:
        container_polygon = Polygon(list(zip(self.Container.X_cor, self.Container.Y_cor)))
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)

        candidate_positions = [(min(self.Container.X_cor), min(self.Container.Y_cor))]  # Start with the bottom-left corner

        for poly in occupied_spaces:
            minx, miny, maxx, maxy = poly.bounds
            candidate_positions.append((minx + shape_width, miny))  # Right of the shape
            candidate_positions.append((minx, miny + shape_height))  # Above the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[1], pos[0]))  # Sort by y, then by x

        for x, y in candidate_positions:
            shape_polygon = self.create_shape_polygon(shape, x, y)
            if container_polygon.contains(shape_polygon) and not any(shape_polygon.intersects(occupied) for occupied in occupied_spaces):
                return x, y

            logging.debug(f"Checking position ({x}, {y}) for shape {shape.Index}.")

        return None, None

    def create_shape_polygon(self, shape: Shape, x_offset: int, y_offset: int) -> Polygon:
        vertices = [(x + x_offset, y + y_offset) for x, y in zip(shape.X_cor, shape.Y_cor)]
        return Polygon(vertices)
