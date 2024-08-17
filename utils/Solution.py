import json
from matplotlib import pyplot as plt, patches
from shapely.geometry import Polygon
from .Container import Container
from .Shape import Shape

PLOT_OFFSET = 300

class Solution:
    """
    A class representing a solution for packing shapes into a container.

    Attributes:
        Type (str): The type of the solution.
        Name (str): The name of the instance.
        Meta (dict[str:str]): Metadata associated with the solution.
        Container (Container): The container in which the shapes are packed.
        Shapes (list[Shape]): A list of shapes included in the solution.
    """

    def __init__(self, type: str, name: str, meta: dict[str:str], cont: Container, shapes: list[Shape]):
        """
        Initializes the Solution class with type, name, metadata, container, and shapes.

        Args:
            type (str): The type of the solution.
            name (str): The name of the instance.
            meta (dict[str:str]): Metadata associated with the solution.
            cont (Container): The container in which the shapes are packed.
            shapes (list[Shape]): A list of shapes included in the solution.
        """
        self.Type = type
        self.Name = name
        self.Meta = meta
        self.Container = cont
        self.Shapes = shapes

    def __str__(self):
        """
        Returns a string representation of the solution, including the number of shapes and total value.

        Returns:
            str: A string representing the solution's details.
        """
        str_representation = f"Selected {len(self.Shapes)} shapes. Total value: {self.grade()}\n"
        for shape in self.Shapes:
            str_representation += f"{shape}\n"
        return str_representation

    def export_to_json(self) -> json:
        """
        Serializes the solution to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary containing the solution's type, name, number of included items, metadata, item indices, and translations.
        """
        item_indices = [item.Index for item in self.Shapes]
        y_translations = [item.Y_offset for item in self.Shapes]
        x_translations = [item.X_offset for item in self.Shapes]
        json_data = {
            "type": self.Type,
            "instance_name": self.Name,
            "num_included_items": len(self.Shapes),
            "meta": self.Meta,
            "item_indices": item_indices,
            "x_translations": x_translations,
            "y_translations": y_translations
        }
        return json_data

    def is_valid(self) -> bool:
        """
        Validates the solution by checking if all shapes are within the container and do not overlap.

        Returns:
            bool: True if the solution is valid, False otherwise.
        """
        container_polygon = Polygon(list(zip(self.Container.X_cor, self.Container.Y_cor)))
        for item1 in self.Shapes:
            item1_polygon = item1.create_polygon_object()
            if not container_polygon.contains(item1_polygon):
                return False
            for item2 in self.Shapes:
                item2_polygon = item2.create_polygon_object()
                if item1 != item2 and item1_polygon.intersects(item2_polygon):
                    return False
        return True

    def visualize_solution(self) -> None:
        """
        Visualizes the solution by plotting the container and shapes using Matplotlib.
        """
        fig, ax = plt.subplots()
        ax.cla()

        # Set title with data about the solution
        ax.set_title(f"Solution: {self.Name}\nValue of solution: {self.grade():,}\nNumber of shapes: {len(self.Shapes)}")

        # Plot the container
        container_polygon = patches.Polygon(list(zip(self.Container.X_cor, self.Container.Y_cor)), closed=True,
                                            edgecolor='black', alpha=0.4)
        ax.add_patch(container_polygon)

        # Collect all coordinates for container and items
        all_x_coords = self.Container.X_cor[:]
        all_y_coords = self.Container.Y_cor[:]

        for shape in self.Shapes:
            item_x, item_y = shape.get_real_coords()

            all_x_coords.extend(item_x)
            all_y_coords.extend(item_y)

            item_polygon = patches.Polygon(list(zip(item_x, item_y)), closed=True, edgecolor='red', alpha=0.4)
            ax.add_patch(item_polygon)

        # Set plot limits based on all coordinates
        ax.set_xlim([min(all_x_coords) - PLOT_OFFSET, max(all_x_coords) + PLOT_OFFSET])
        ax.set_ylim([min(all_y_coords) - PLOT_OFFSET, max(all_y_coords) + PLOT_OFFSET])
        ax.set_aspect('equal', adjustable='box')  # Equal aspect ratio for x and y axes

        plt.show()

    def grade(self) -> int:
        """
        Calculates the total value of the solution by summing the values of all included shapes.

        Returns:
            int: The total value of the solution.
        """
        grade = 0
        for shape in self.Shapes:
            grade += shape.real_value
        return grade

    def get_remaining_area_in_container(self) -> float:
        """
        Calculates the remaining area in the container after placing all the shapes.

        Returns:
            float: The remaining area in the container.
        """
        remaining_area = self.Container.get_area()
        for item in self.Shapes:
            remaining_area -= item.get_area()
        return remaining_area
