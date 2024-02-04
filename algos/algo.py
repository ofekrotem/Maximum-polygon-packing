from utils.Solution import Solution
from utils.Shape import Shape
from utils.Container import Container
from enum import Enum
import random
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


    # 2 variatons of this function, controlled by 'classification' arg:
    # 1. "random" - for a random order scan of the shapes list
    # 2. "sort by area" - for an increasing area scan of the shapes list
    # 3. "sort by value" - for an decreasing value scan of the shapes list
    def create_random_offset_solution(self, classification: str) -> Solution:
        s = Solution(TYPE, NAME, META, [], [], [], self.Container, self.Shapes)
        solution_shapes_list = self.Shapes

        if classification == AlgoClassification.RANDOM:
            print("Random shapes list")
            solution_shapes_list = self.ShuffledShapes
        elif classification == AlgoClassification.SORT_BY_AREA:
            print("Sorted by area")
            solution_shapes_list = self.SortedbyAreaShapes
        elif classification == AlgoClassification.SORT_BY_VALUE:
            print("Sorted by value")
            solution_shapes_list = self.SortedbyValueShapes

        for shape in solution_shapes_list:
            min_x, min_y, max_x, max_y = self.find_ranges(shape)
            print(f"Shape {shape.Index}, Ranges: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y}")

            for i in range(self.TriesOnRandomCreation):
                x_sample = random.randint(min_x, max_x)
                y_sample = random.randint(min_y, max_y)
                print(f"Trying to place {shape.Index} with Ranges: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y} at ({x_sample}, {y_sample})")
                s.X_Offset.append(x_sample)
                s.Y_Offset.append(y_sample)
                s.Items_ID.append(shape.Index)

                ans = s.is_valid()
                if ans:
                    print(f"Placed shape {shape.Index} successfully at ({x_sample}, {y_sample})")
                    break
                else:
                    s.X_Offset.pop()
                    s.Y_Offset.pop()
                    s.Items_ID.pop()
        # print(s)
        return s

