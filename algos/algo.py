import copy
import logging
from utils.Solution import Solution
from utils.Shape import Shape
from utils.Container import Container
from enum import Enum
import random
from shapely.geometry import Polygon, Point

random.seed(0)

# Consts
TYPE = "cgshop2024_solution"
NAME = "atris42"
META = {"approach": "generated solution"}

class SortClassification(Enum):
    RANDOM = "random"
    SORT_BY_AREA = "sort_by_area"
    SORT_BY_VALUE = "sort_by_value"
    SORT_BY_PERIMETER = "sort_by_perimeter"

class FindPositionClassification(Enum):
    BOTTOM_LEFT = "bottom_left"
    TOP_LEFT = "top_left"
    BOTTOM_RIGHT = "bottom_right"
    TOP_RIGHT = "top_right"

class Algo:
    def __init__(self, shapes: list[Shape], cont: Container, tries_on_random_creation: int = 100):
        self.Shapes = shapes
        self.Container = cont
        self.TriesOnRandomCreation = tries_on_random_creation

    def sort_shapes_by_value(self,shapes_list) -> list[Shape]:
        shapes_copy = copy.deepcopy(shapes_list)
        return sorted(shapes_copy, key=lambda s: s.Value, reverse=True)

    def sort_shapes_by_area(self,shapes_list) -> list[Shape]:
        shapes_copy = copy.deepcopy(shapes_list)
        return sorted(shapes_copy, key=lambda s: s.get_area())

    def shuffle_shape_list(self,shapes_list) -> list[Shape]:
        shapes_copy = copy.deepcopy(shapes_list)
        shuffled = shapes_copy[:]
        random.shuffle(shuffled)
        return shuffled

    def sort_by_perimeter(self,shapes_list) -> list[Shape]:
        shapes_copy = copy.deepcopy(shapes_list)
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

    def create_random_offset_solution(self) -> Solution:
        s = Solution(TYPE, NAME, META, self.Container, [])
        solution_shapes_list = self.shuffle_shape_list(self.Shapes)

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
                logging.debug(f"Could not place shape {shape.Index} after {self.TriesOnRandomCreation} tries.")

        logging.debug(s)
        return s

    def create_bottom_left_solution(self) -> Solution:
        s = Solution(TYPE, NAME, META, self.Container, [])
        sorted_shapes = self.sort_shapes_by_value(self.Shapes)
        logging.debug(f"Starting bottom-left placement with {len(sorted_shapes)} shapes.")
        print(f"Starting bottom-left placement with {len(sorted_shapes)} shapes.")
        for shape in sorted_shapes:
            x, y = self.find_bottom_left_position(shape,s)
            if x is not None and y is not None:
                logging.debug(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                logging.debug(f"Could not place shape {shape.Index}. No valid position found.")
        print(f"Finished bottom-left placement with {len(s.Shapes)} shapes.")
        logging.debug(f"Final Solution: {s}")
        return s

    def create_top_left_solution(self) -> Solution:
        s = Solution(TYPE, NAME, META, self.Container, [])
        sorted_shapes = self.sort_shapes_by_value(self.Shapes)
        logging.debug(f"Starting top-left placement with {len(sorted_shapes)} shapes.")
        print(f"Starting top-left placement with {len(sorted_shapes)} shapes.")
        for shape in sorted_shapes:
            x, y = self.find_top_left_position(shape,s)
            if x is not None and y is not None:
                logging.debug(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                logging.debug(f"Could not place shape {shape.Index}. No valid position found.")
        print(f"Finished top-left placement with {len(s.Shapes)} shapes.")
        logging.debug(f"Final Solution: {s}")
        return s

    def create_top_right_solution(self) -> Solution:
        s = Solution(TYPE, NAME, META, self.Container, [])
        sorted_shapes = self.sort_shapes_by_value(self.Shapes)
        logging.debug(f"Starting top-right placement with {len(sorted_shapes)} shapes.")
        print(f"Starting top-right placement with {len(sorted_shapes)} shapes.")
        for shape in sorted_shapes:
            x, y = self.find_top_right_position(shape,s)
            if x is not None and y is not None:
                logging.debug(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                logging.debug(f"Could not place shape {shape.Index}. No valid position found.")
        print(f"Finished top-right placement with {len(s.Shapes)} shapes.")
        logging.debug(f"Final Solution: {s}")
        return s

    def create_bottom_right_solution(self) -> Solution:
        s = Solution(TYPE, NAME, META, self.Container, [])
        sorted_shapes = self.sort_shapes_by_value(self.Shapes)
        print(f"Starting bottom-right placement with {len(sorted_shapes)} shapes.")
        logging.debug(f"Starting bottom-right placement with {len(sorted_shapes)} shapes.")
        for shape in sorted_shapes:
            x, y = self.find_bottom_right_position(shape,s)
            if x is not None and y is not None:
                logging.debug(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                logging.debug(f"Could not place shape {shape.Index}. No valid position found.")
        print(f"Finished bottom-right placement with {len(s.Shapes)} shapes.")
        logging.debug(f"Final Solution: {s}")
        return s

    def find_bottom_left_position(self, shape: Shape,curr_solution: Solution) -> tuple[int, int]:
        min_x = min(self.Container.X_cor)
        real_min_y = min(self.Container.Y_cor)
        y_of_min_x =  max(self.Container.Y_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if x == min_x and y < y_of_min_x:
                y_of_min_x = y
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(min_x,real_min_y), (min_x + shape_width, y_of_min_x + shape_height)]  # Start with the bottom-left corner
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            logging.debug(f"Shape {located_shape.Index} bounds: minx={minx}, miny={miny}")

            candidate_positions.append((maxx+1, miny+1))  # Right of the shape
            candidate_positions.append((minx+1, maxy+1))  # Above the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[1], pos[0]))  # Sort by y, then by x

        for x, y in candidate_positions:
            candidate_point = Point(x,y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - min(shape.X_cor)
            possible_y_offset = y - min(shape.Y_cor)
            logging.debug(f"Checking position ({x}, {y}) for shape {shape.Index}.")
            shape.X_offset = possible_x_offset
            shape.Y_offset = possible_y_offset
            curr_solution.Shapes.append(shape)
            is_valid = curr_solution.is_valid()
            if is_valid:
                return possible_x_offset, possible_y_offset
            else:
                shape.X_offset = 0
                shape.Y_offset = 0
                curr_solution.Shapes.remove(shape)

        return None, None

    def find_top_left_position(self, shape: Shape,curr_solution: Solution) -> tuple[int, int]:
        min_x = min(self.Container.X_cor)
        real_max_y = max(self.Container.Y_cor)
        y_of_min_x =  min(self.Container.Y_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if x == min_x and y > y_of_min_x:
                y_of_min_x = y
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(min_x,real_max_y), (min_x + shape_width, y_of_min_x - shape_height)]
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            logging.debug(f"Shape {located_shape.Index} bounds: minx={minx}, miny={miny}")
            candidate_positions.append((maxx+1, maxy-1)) # Right of the shape
            candidate_positions.append((minx+1, miny-1)) # Below the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[1], pos[0]), reverse=True)  # Sort by y, then by x

        for x, y in candidate_positions:
            candidate_point = Point(x,y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - min(shape.X_cor)
            possible_y_offset = y - max(shape.Y_cor)
            logging.debug(f"Checking position ({x}, {y}) for shape {shape.Index}.")
            shape.X_offset = possible_x_offset
            shape.Y_offset = possible_y_offset
            curr_solution.Shapes.append(shape)
            is_valid = curr_solution.is_valid()
            if is_valid:
                return possible_x_offset, possible_y_offset
            else:
                shape.X_offset = 0
                shape.Y_offset = 0
                curr_solution.Shapes.remove(shape)

        return None, None

    def find_top_right_position(self, shape: Shape,curr_solution: Solution) -> tuple[int, int]:
        max_y = max(self.Container.Y_cor)
        real_max_x = max(self.Container.X_cor)
        x_of_max_y =  min(self.Container.X_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if y == max_y and x > x_of_max_y:
                x_of_max_y = x
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(real_max_x,max_y), (x_of_max_y - shape_width, max_y - shape_height)]
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            logging.debug(f"Shape {located_shape.Index} bounds: minx={minx}, miny={miny}")
            candidate_positions.append((minx-1, maxy-1)) # Left of the shape
            candidate_positions.append((maxx-1, miny-1)) # Below the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[0], pos[1]), reverse=True)  # Sort by x, then by y

        for x, y in candidate_positions:
            candidate_point = Point(x,y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - max(shape.X_cor)
            possible_y_offset = y - max(shape.Y_cor)
            logging.debug(f"Checking position ({x}, {y}) for shape {shape.Index}.")
            shape.X_offset = possible_x_offset
            shape.Y_offset = possible_y_offset
            curr_solution.Shapes.append(shape)
            is_valid = curr_solution.is_valid()
            if is_valid:
                return possible_x_offset, possible_y_offset
            else:
                shape.X_offset = 0
                shape.Y_offset = 0
                curr_solution.Shapes.remove(shape)

        return None, None

    def find_bottom_right_position(self, shape: Shape,curr_solution: Solution) -> tuple[int, int]:
        min_y = min(self.Container.Y_cor)
        real_max_x = max(self.Container.X_cor)
        x_of_min_y =  min(self.Container.X_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if y == min_y and x > x_of_min_y:
                x_of_min_y = x
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(real_max_x,min_y), (x_of_min_y - shape_width, min_y + shape_height)]
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            logging.debug(f"Shape {located_shape.Index} bounds: minx={minx}, miny={miny}")
            candidate_positions.append((minx-1, miny+1)) # Left of the shape
            candidate_positions.append((maxx-1, maxy+1)) # Above the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[0], pos[1]), reverse=True)  # Sort by x, then by y

        for x, y in candidate_positions:
            candidate_point = Point(x,y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - max(shape.X_cor)
            possible_y_offset = y - min(shape.Y_cor)
            logging.debug(f"Checking position ({x}, {y}) for shape {shape.Index}.")
            shape.X_offset = possible_x_offset
            shape.Y_offset = possible_y_offset
            curr_solution.Shapes.append(shape)
            is_valid = curr_solution.is_valid()
            if is_valid:
                return possible_x_offset, possible_y_offset
            else:
                shape.X_offset = 0
                shape.Y_offset = 0
                curr_solution.Shapes.remove(shape)

        return None, None

    def push_shapes_left(self, solution: Solution) -> Solution:
        # Mutation: Push polygons left if possible while maintaining validity
        logging.debug(f"Pushing shapes left {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[0]))

        for shape in solution_shapes_sorted:
            left_limit = min(solution.Container.X_cor)
            right_limit = min(shape.get_real_coords()[0])
            while left_limit + 0.5 < right_limit - 0.5:
                sample_x = (left_limit + right_limit) // 2
                original_x_offset = shape.X_offset
                shape.X_offset += sample_x - right_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} left to {sample_x}")
                    right_limit = sample_x
                else:
                    shape.X_offset = original_x_offset
                    left_limit = sample_x
        return mutated_solution


    def push_shapes_down(self, solution: Solution) -> Solution:
        # Mutation: Push polygons down if possible while maintaining validity
        logging.debug(f"Pushing shapes down {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[1]))

        for shape in solution_shapes_sorted:
            bottom_limit = min(solution.Container.Y_cor)
            top_limit = min(shape.get_real_coords()[1])
            while bottom_limit + 0.5 < top_limit - 0.5:
                sample_y = (bottom_limit + top_limit) // 2
                original_y_offset = shape.Y_offset
                shape.Y_offset += sample_y - top_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} down to {sample_y}")
                    top_limit = sample_y
                else:
                    shape.Y_offset = original_y_offset
                    bottom_limit = sample_y

        return mutated_solution

    def push_shapes_up(self,solution: Solution) -> Solution:
        # Mutation: Push polygons up if possible while maintaining validity
        logging.debug(f"Pushing shapes up {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[1]), reverse=True)

        for shape in solution_shapes_sorted:
            top_limit = max(solution.Container.Y_cor)
            bottom_limit = max(shape.get_real_coords()[1])
            while bottom_limit + 0.5 < top_limit - 0.5:
                sample_y = (bottom_limit + top_limit) // 2
                original_y_offset = shape.Y_offset
                shape.Y_offset += sample_y - bottom_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} up to {sample_y}")
                    bottom_limit = sample_y
                else:
                    shape.Y_offset = original_y_offset
                    top_limit = sample_y

        return mutated_solution

    def push_shapes_right(self, solution: Solution) -> Solution:
        # Mutation: Push polygons right if possible while maintaining validity
        logging.debug(f"Pushing shapes right {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[0]), reverse=True)

        for shape in solution_shapes_sorted:
            right_limit = max(solution.Container.X_cor)
            left_limit = max(shape.get_real_coords()[0])
            while left_limit + 0.5 < right_limit - 0.5:
                sample_x = (left_limit + right_limit) // 2
                original_x_offset = shape.X_offset
                shape.X_offset += sample_x - left_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} left to {sample_x}")
                    left_limit = sample_x
                else:
                    shape.X_offset = original_x_offset
                    right_limit = sample_x
        return mutated_solution

    def fit_remaining_shapes_in_solution(self, solution: Solution,classification: FindPositionClassification) -> Solution:
        solution_copy = copy.deepcopy(solution)
        solution_shape_ids = [shape.Index for shape in solution_copy.Shapes]
        remaining_shapes = [shape for shape in self.Shapes if shape.Index not in solution_shape_ids]
        remaining_shapes = self.sort_shapes_by_value(remaining_shapes)

        for shape in remaining_shapes:
            remaining_area = solution_copy.get_remaining_area_in_container()
            if shape.get_area() > remaining_area:
                logging.debug(f"Could not place shape {shape.Index}. Not enough space left.")
                continue
            if classification == FindPositionClassification.BOTTOM_LEFT:
                x, y = self.find_bottom_left_position(shape, solution_copy)
            elif classification == FindPositionClassification.TOP_LEFT:
                x, y = self.find_top_left_position(shape, solution_copy)
            elif classification == FindPositionClassification.BOTTOM_RIGHT:
                x, y = self.find_bottom_right_position(shape, solution_copy)
            elif classification == FindPositionClassification.TOP_RIGHT:
                x, y = self.find_top_right_position(shape, solution_copy)
            if x is not None and y is not None:
                logging.debug(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                logging.debug(f"Could not place shape {shape.Index}. No valid position found.")

        return solution_copy

    def create_shape_polygon(self, shape: Shape, x_offset: int, y_offset: int) -> Polygon:
        vertices = [(x + x_offset, y + y_offset) for x, y in zip(shape.X_cor, shape.Y_cor)]
        return Polygon(vertices)

