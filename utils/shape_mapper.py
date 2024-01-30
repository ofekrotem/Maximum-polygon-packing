from prompt_toolkit.filters import is_true
from Soultion import Solution
from z3 import *


class ShapeMapper:
    def __init__(self):
        self.shape_placed = []
        self.x_offset = []
        self.y_offset = []
        self.container = None

    def solve(self, container, shapes):
        # Create Z3 solver
        solver = Optimize()

        # Define decision variables
        self.shape_placed = [Bool(f"shape_{i}_placed") for i in range(len(shapes))]
        self.x_offset = [Int(f"shape_{i}_x_offset") for i in range(len(shapes))]
        self.y_offset = [Int(f"shape_{i}_y_offset") for i in range(len(shapes))]
        self.container = container

        # Define objective function
        total_value = Sum([If(self.shape_placed[i], shapes[i].Value, 0) for i in range(len(shapes))])
        solver.maximize(total_value)

        # Define constraints
        for i in range(len(shapes)):
            # Overlapping constraint
            for j in range(i):
                solver.add(
                    Or(Not(self.shape_placed[i]), Not(self.shape_placed[j]),
                       Not(shapes[i].Polygon.intersects(shapes[j].Polygon))))

            # Boundary constraint
            for vertex_x, vertex_y in zip(shapes[i].X_cor, shapes[i].Y_cor):
                solver.add(
                    Or(
                        Not(self.shape_placed[i]),
                        And(
                            vertex_x + self.x_offset[i] >= container.X_cor[0],
                            vertex_x + self.x_offset[i] <= container.X_cor[-1],
                            vertex_y + self.y_offset[i] >= container.Y_cor[0],
                            vertex_y + self.y_offset[i] <= container.Y_cor[-1]
                        )
                    )
                )

            # Non-rotational constraint
            x_aligned = And([vertex_y == shapes[i].Y_cor[0] for vertex_y in shapes[i].Y_cor])
            y_aligned = And([vertex_x == shapes[i].X_cor[0] for vertex_x in shapes[i].X_cor])
            solver.add(Or(Not(self.shape_placed[i]), x_aligned, y_aligned))

        # Solve the model
        if solver.check() == sat:
            model = solver.model()
            solution = self.extract_solution(model, container, shapes)
            return solution
        else:
            print("No feasible solution found.")
        return None

    def extract_solution(self, model, container, shapes):
        shape_indices = []
        x_offsets = []
        y_offsets = []

        for i, shape in enumerate(shapes):
            if is_true(model[self.shape_placed[i]]):
                shape_indices.append(shape.Index)
                x_offsets.append(model[self.x_offset[i]].as_long())
                y_offsets.append(model[self.y_offset[i]].as_long())

        solution = Solution("shape_mapping", container.Instance_Name, len(shape_indices), "Some metadata",
                            shape_indices, x_offsets, y_offsets)

        return solution


