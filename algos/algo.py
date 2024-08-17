import copy
from utils.Solution import Solution
from utils.Shape import Shape
from utils.Container import Container
from enum import Enum
import random
from shapely.geometry import Polygon, Point

random.seed(0)

# Consts
TYPE = "cgshop2024_solution"
META = {"approach": "Genetic algorithm solution"}

class SortClassification(Enum):
    """Enum for classifying different sorting methods."""
    RANDOM = "random"
    SORT_BY_AREA = "sort_by_area"
    SORT_BY_VALUE = "sort_by_value"
    SORT_BY_PERIMETER = "sort_by_perimeter"

class FindPositionClassification(Enum):
    """Enum for classifying different position finding methods."""
    BOTTOM_LEFT = "bottom_left"
    TOP_LEFT = "top_left"
    BOTTOM_RIGHT = "bottom_right"
    TOP_RIGHT = "top_right"

class Algo:
    """
    Base class for algorithms involving shapes and containers.

    Attributes:
        Shapes (list[Shape]): List of shapes to be packed.
        Container (Container): The container in which the shapes should be packed.
        TriesOnRandomCreation (int): Number of tries allowed for random solution creation.
    """
    def __init__(self, shapes: list[Shape], cont: Container, tries_on_random_creation: int = 100,instance_name: str = ""):
        """
        Initializes the Algo class with shapes, container, and number of tries for random creation.

        Args:
            shapes (list[Shape]): List of shapes to be packed.
            cont (Container): The container in which the shapes should be packed.
            tries_on_random_creation (int): Number of tries allowed for random solution creation.
            instance_name (str): The name of the instance for identification.
        """
        self.Shapes = shapes
        self.Container = cont
        self.TriesOnRandomCreation = tries_on_random_creation
        self.Instance_Name = instance_name

    def sort_shapes_by_value(self, shapes_list) -> list[Shape]:
        """
        Sorts a list of shapes by their value in descending order.

        Args:
            shapes_list (list[Shape]): List of shapes to be sorted.

        Returns:
            list[Shape]: A new list of shapes sorted by value.
        """
        shapes_copy = copy.deepcopy(shapes_list)
        return sorted(shapes_copy, key=lambda s: s.Value, reverse=True)

    def sort_shapes_by_real_value(self, shapes_list) -> list[Shape]:
        """
        Sorts a list of shapes by their real value in descending order.

        Args:
            shapes_list (list[Shape]): List of shapes to be sorted.

        Returns:
            list[Shape]: A new list of shapes sorted by real value.
        """
        shapes_copy = copy.deepcopy(shapes_list)
        return sorted(shapes_copy, key=lambda s: s.real_value, reverse=True)

    def sort_shapes_by_area(self, shapes_list) -> list[Shape]:
        """
        Sorts a list of shapes by their area in ascending order.

        Args:
            shapes_list (list[Shape]): List of shapes to be sorted.

        Returns:
            list[Shape]: A new list of shapes sorted by area.
        """
        shapes_copy = copy.deepcopy(shapes_list)
        return sorted(shapes_copy, key=lambda s: s.get_area())

    def shuffle_shape_list(self, shapes_list) -> list[Shape]:
        """
        Shuffles the list of shapes randomly.

        Args:
            shapes_list (list[Shape]): List of shapes to be shuffled.

        Returns:
            list[Shape]: A new list of shuffled shapes.
        """
        shapes_copy = copy.deepcopy(shapes_list)
        shuffled = shapes_copy[:]
        random.shuffle(shuffled)
        return shuffled

    def sort_by_perimeter(self, shapes_list) -> list[Shape]:
        """
        Sorts a list of shapes by their perimeter in ascending order.

        Args:
            shapes_list (list[Shape]): List of shapes to be sorted.

        Returns:
            list[Shape]: A new list of shapes sorted by perimeter.
        """
        shapes_copy = copy.deepcopy(shapes_list)
        return sorted(shapes_copy, key=lambda s: s.get_perimeter())

    def find_ranges(self, s: Shape) -> tuple[int, int, int, int]:
        """
        Calculates the valid range for placing a shape within the container.

        Args:
            s (Shape): The shape for which to find the ranges.

        Returns:
            tuple[int, int, int, int]: The minimum and maximum x and y offsets within which the shape can be placed.
        """
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

    def create_random_offset_solution(self, shapes_list) -> Solution:
        """
        Creates a solution by placing shapes at random offsets within the container.

        Args:
            shapes_list (list[Shape]): List of shapes to be placed.

        Returns:
            Solution: A solution containing the placed shapes.
        """
        s = Solution(TYPE, self.Instance_Name, META, self.Container, [])
        solution_shapes_list = self.shuffle_shape_list(shapes_list)

        for shape in solution_shapes_list:
            min_x, min_y, max_x, max_y = self.find_ranges(shape)

            for i in range(self.TriesOnRandomCreation):
                x_sample = random.randint(min_x, max_x)
                y_sample = random.randint(min_y, max_y)
                shape.X_offset = x_sample
                shape.Y_offset = y_sample
                s.Shapes.append(shape)

                ans = s.is_valid()
                if ans:
                    break
                else:
                    shape.X_offset = 0
                    shape.Y_offset = 0
                    s.Shapes.remove(shape)

        return s

    def create_bottom_left_solution(self, sorted_shapes) -> Solution:
        """
        Creates a solution by placing shapes starting from the bottom-left corner of the container.

        Args:
            sorted_shapes (list[Shape]): List of shapes sorted for placement.

        Returns:
            Solution: A solution containing the placed shapes.
        """
        s = Solution(TYPE, self.Instance_Name, META, self.Container, [])
        for shape in sorted_shapes:
            self.find_bottom_left_position(shape, s)
        return s

    def create_top_left_solution(self, sorted_shapes) -> Solution:
        """
        Creates a solution by placing shapes starting from the top-left corner of the container.

        Args:
            sorted_shapes (list[Shape]): List of shapes sorted for placement.

        Returns:
            Solution: A solution containing the placed shapes.
        """
        s = Solution(TYPE, self.Instance_Name, META, self.Container, [])
        for shape in sorted_shapes:
            self.find_top_left_position(shape, s)
        return s

    def create_top_right_solution(self, sorted_shapes) -> Solution:
        """
        Creates a solution by placing shapes starting from the top-right corner of the container.

        Args:
            sorted_shapes (list[Shape]): List of shapes sorted for placement.

        Returns:
            Solution: A solution containing the placed shapes.
        """
        s = Solution(TYPE, self.Instance_Name, META, self.Container, [])
        for shape in sorted_shapes:
            self.find_top_right_position(shape, s)
        return s

    def create_bottom_right_solution(self, sorted_shapes) -> Solution:
        """
        Creates a solution by placing shapes starting from the bottom-right corner of the container.

        Args:
            sorted_shapes (list[Shape]): List of shapes sorted for placement.

        Returns:
            Solution: A solution containing the placed shapes.
        """
        s = Solution(TYPE, self.Instance_Name, META, self.Container, [])
        for shape in sorted_shapes:
            self.find_bottom_right_position(shape, s)
        return s

    def find_bottom_left_position(self, shape: Shape, curr_solution: Solution) -> tuple[int, int]:
        """
        Finds the best bottom-left position for a shape within the current solution.

        Args:
            shape (Shape): The shape to be placed.
            curr_solution (Solution): The current solution to which the shape will be added.

        Returns:
            tuple[int, int]: The x and y offsets for placing the shape, or (None, None) if no valid position is found.
        """
        min_x = min(self.Container.X_cor)
        real_min_y = min(self.Container.Y_cor)
        y_of_min_x = max(self.Container.Y_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if x == min_x and y < y_of_min_x:
                y_of_min_x = y
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(min_x, real_min_y), (min_x + shape_width, y_of_min_x + shape_height)]  # Start with the bottom-left corner
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds

            candidate_positions.append((maxx + 1, miny + 1))  # Right of the shape
            candidate_positions.append((minx + 1, maxy + 1))  # Above the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[1], pos[0]))  # Sort by y, then by x

        for x, y in candidate_positions:
            candidate_point = Point(x, y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - min(shape.X_cor)
            possible_y_offset = y - min(shape.Y_cor)
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

    def find_top_left_position(self, shape: Shape, curr_solution: Solution) -> tuple[int, int]:
        """
        Finds the best top-left position for a shape within the current solution.

        Args:
            shape (Shape): The shape to be placed.
            curr_solution (Solution): The current solution to which the shape will be added.

        Returns:
            tuple[int, int]: The x and y offsets for placing the shape, or (None, None) if no valid position is found.
        """
        min_x = min(self.Container.X_cor)
        real_max_y = max(self.Container.Y_cor)
        y_of_min_x = min(self.Container.Y_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if x == min_x and y > y_of_min_x:
                y_of_min_x = y
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(min_x, real_max_y), (min_x + shape_width, y_of_min_x - shape_height)]
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            candidate_positions.append((maxx + 1, maxy - 1))  # Right of the shape
            candidate_positions.append((minx + 1, miny - 1))  # Below the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[1], pos[0]), reverse=True)  # Sort by y, then by x

        for x, y in candidate_positions:
            candidate_point = Point(x, y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - min(shape.X_cor)
            possible_y_offset = y - max(shape.Y_cor)
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

    def find_top_right_position(self, shape: Shape, curr_solution: Solution) -> tuple[int, int]:
        """
        Finds the best top-right position for a shape within the current solution.

        Args:
            shape (Shape): The shape to be placed.
            curr_solution (Solution): The current solution to which the shape will be added.

        Returns:
            tuple[int, int]: The x and y offsets for placing the shape, or (None, None) if no valid position is found.
        """
        max_y = max(self.Container.Y_cor)
        real_max_x = max(self.Container.X_cor)
        x_of_max_y = min(self.Container.X_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if y == max_y and x > x_of_max_y:
                x_of_max_y = x
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(real_max_x, max_y), (x_of_max_y - shape_width, max_y - shape_height)]
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            candidate_positions.append((minx - 1, maxy - 1))  # Left of the shape
            candidate_positions.append((maxx - 1, miny - 1))  # Below the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[0], pos[1]), reverse=True)  # Sort by x, then by y

        for x, y in candidate_positions:
            candidate_point = Point(x, y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - max(shape.X_cor)
            possible_y_offset = y - max(shape.Y_cor)
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

    def find_bottom_right_position(self, shape: Shape, curr_solution: Solution) -> tuple[int, int]:
        """
        Finds the best bottom-right position for a shape within the current solution.

        Args:
            shape (Shape): The shape to be placed.
            curr_solution (Solution): The current solution to which the shape will be added.

        Returns:
            tuple[int, int]: The x and y offsets for placing the shape, or (None, None) if no valid position is found.
        """
        min_y = min(self.Container.Y_cor)
        real_max_x = max(self.Container.X_cor)
        x_of_min_y = min(self.Container.X_cor)
        for x, y in zip(self.Container.X_cor, self.Container.Y_cor):
            if y == min_y and x > x_of_min_y:
                x_of_min_y = x
        shape_width = max(shape.X_cor) - min(shape.X_cor)
        shape_height = max(shape.Y_cor) - min(shape.Y_cor)
        candidate_positions = [(real_max_x, min_y), (x_of_min_y - shape_width, min_y + shape_height)]
        for located_shape in curr_solution.Shapes:
            poly = located_shape.create_polygon_object()
            minx, miny, maxx, maxy = poly.bounds
            candidate_positions.append((minx - 1, miny + 1))  # Left of the shape
            candidate_positions.append((maxx - 1, maxy + 1))  # Above the shape

        candidate_positions = sorted(set(candidate_positions), key=lambda pos: (pos[0], pos[1]), reverse=True)  # Sort by x, then by y

        for x, y in candidate_positions:
            candidate_point = Point(x, y)
            for located_shape in curr_solution.Shapes:
                poly = located_shape.create_polygon_object()
                if poly.contains(candidate_point):
                    continue
            possible_x_offset = x - max(shape.X_cor)
            possible_y_offset = y - min(shape.Y_cor)
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
        """
        Mutates a solution by pushing shapes to the left as much as possible while maintaining validity.

        Args:
            solution (Solution): The current solution to mutate.

        Returns:
            Solution: The mutated solution with shapes pushed to the left.
        """
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
                    right_limit = sample_x
                else:
                    shape.X_offset = original_x_offset
                    left_limit = sample_x
        return mutated_solution


    def push_shapes_down(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes down as much as possible while maintaining validity.

        Args:
            solution (Solution): The current solution to mutate.

        Returns:
            Solution: The mutated solution with shapes pushed down.
        """
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
                    top_limit = sample_y
                else:
                    shape.Y_offset = original_y_offset
                    bottom_limit = sample_y

        return mutated_solution

    def push_shapes_up(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes up as much as possible while maintaining validity.

        Args:
            solution (Solution): The current solution to mutate.

        Returns:
            Solution: The mutated solution with shapes pushed up.
        """
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
                    bottom_limit = sample_y
                else:
                    shape.Y_offset = original_y_offset
                    top_limit = sample_y

        return mutated_solution

    def push_shapes_right(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes to the right as much as possible while maintaining validity.

        Args:
            solution (Solution): The current solution to mutate.

        Returns:
            Solution: The mutated solution with shapes pushed to the right.
        """
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
                    left_limit = sample_x
                else:
                    shape.X_offset = original_x_offset
                    right_limit = sample_x
        return mutated_solution

    def fit_remaining_shapes_in_solution(self, solution: Solution, classification: FindPositionClassification) -> Solution:
        """
        Attempts to fit remaining shapes into the solution based on a specified classification.

        Args:
            solution (Solution): The current solution.
            classification (FindPositionClassification): The classification method for fitting the shapes.

        Returns:
            Solution: The solution with as many remaining shapes as possible fit in.
        """
        solution_copy = copy.deepcopy(solution)
        solution_shape_ids = [shape.Index for shape in solution_copy.Shapes]
        remaining_shapes = [shape for shape in self.Shapes if shape.Index not in solution_shape_ids]
        remaining_shapes = self.sort_shapes_by_value(remaining_shapes)

        for shape in remaining_shapes:
            remaining_area = solution_copy.get_remaining_area_in_container()
            if shape.get_area() > remaining_area:
                continue
            if classification == FindPositionClassification.BOTTOM_LEFT:
                self.find_bottom_left_position(shape, solution_copy)
            elif classification == FindPositionClassification.TOP_LEFT:
                self.find_top_left_position(shape, solution_copy)
            elif classification == FindPositionClassification.BOTTOM_RIGHT:
                self.find_bottom_right_position(shape, solution_copy)
            elif classification == FindPositionClassification.TOP_RIGHT:
                self.find_top_right_position(shape, solution_copy)


        return solution_copy

    def create_shape_polygon(self, shape: Shape, x_offset: int, y_offset: int) -> Polygon:
        """
        Creates a Shapely Polygon object representing the shape with the given offsets.

        Args:
            shape (Shape): The shape to create a polygon for.
            x_offset (int): The x offset for the shape.
            y_offset (int): The y offset for the shape.

        Returns:
            Polygon: A Shapely Polygon object representing the shape.
        """
        vertices = [(x + x_offset, y + y_offset) for x, y in zip(shape.X_cor, shape.Y_cor)]
        return Polygon(vertices)
