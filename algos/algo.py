from utils.Solution import Solution
from utils.Shape import Shape
from utils.Container import Container
import random

# Consts
TYPE = "cgshop2024_solution"
NAME = "atris42"
META = {"approach": "generated solution"}
TRIES = 2000


class Algo:
    def __init__(self, shapes: list[Shape], cont: Container):
        self.Shapes = shapes
        self.Container = cont
        self.ShuffledShapes = self.shuffle_list()
        self.SortedbyAreaShapes = self.sort_area()

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

        min_x = max(min_container_x, min_container_x - min_shape_x)
        max_x = min(max_container_x, max_container_x - max_shape_x)
        min_y = max(min_container_y, min_container_y - min_shape_y)
        max_y = min(max_container_y, max_container_y - max_shape_y)

        return min_x, min_y, max_x, max_y


    # 2 variatons of this function, controlled by 'classification' arg:
    # 1. "random" - for a random order scan of the shapes list
    # 2. "sort by area" - for an increasing area scan of the shapes list
    def create_random_offset_solution(self, classification: str) -> Solution:
        s = Solution(TYPE, NAME, META, [], [], [], self.Container, self.Shapes)
        solution_shapes_list = self.Shapes

        if classification == "random":
            print("Random shapes list")
            solution_shapes_list = self.ShuffledShapes
        elif classification == "sort by area":
            print("Sorted by area")
            solution_shapes_list = self.SortedbyAreaShapes

        for shape in solution_shapes_list:
            min_x, min_y, max_x, max_y = self.find_ranges(shape)
            print(f"Shape {shape.Index}, Ranges: min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y}")

            for i in range(TRIES):
                x_sample = random.randint(min_x, max_x)
                y_sample = random.randint(min_y, max_y)
                s.X_Offset.append(x_sample)
                s.Y_Offset.append(y_sample)
                s.Items_ID.append(shape.Index)

                ans = s.is_valid()
                if ans:
                    print(f"Placed shape {shape.Index} successfully at ({x_sample}, {y_sample})")
                    break
                else:
                    print(f"Failed attempt {i+1} for shape {shape.Index}")
                    s.X_Offset.pop()
                    s.Y_Offset.pop()
                    s.Items_ID.pop()
        print(s)
        return s

