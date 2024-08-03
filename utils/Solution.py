import json
import logging
from matplotlib import pyplot as plt, patches
from shapely.geometry import Polygon
from .Container import Container
from .Shape import Shape

PLOT_OFFSET = 300


class Solution:
    def __init__(self, type: str, name: str, meta: dict[str:str],cont: Container, shapes: list[Shape]):
        self.Type = type
        self.Name = name
        self.Meta = meta
        self.Container = cont
        self.Shapes = shapes

    def __str__(self):
        str = f"Selected {len(self.Shapes)} shapes. Total value: {self.grade()}\n"
        for shape in self.Shapes:
            str += f"{shape}\n"
        return str

    def export_to_json(self) -> json:
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
        if any(item.Index < 0 for item in self.Shapes):
            logging.error("Negative index found")
            return False


        container_polygon = Polygon(list(zip(self.Container.X_cor, self.Container.Y_cor)))
        for item1 in self.Shapes:
            item1_polygon = item1.create_polygon_object()
            if not container_polygon.contains(item1_polygon):
                logging.debug("Item outside container")
                return False
            for item2 in self.Shapes:
                item2_polygon = item2.create_polygon_object()
                if item1 != item2 and item1_polygon.intersects(item2_polygon):
                    logging.debug("Items intersect")
                    return False
        logging.debug("Solution is valid")
        return True

    def visualize_solution(self) -> None:
        fig, ax = plt.subplots()
        ax.cla()


        # Set title with data about the solution
        ax.set_title(f"Solution: {self.Name}\nValue of solution: {self.grade():,}\nNumber of shapes: {len(self.Shapes)}")

        # Plot the container
        container_polygon = patches.Polygon(list(zip(self.Container.X_cor, self.Container.Y_cor)), closed=True,
                                        edgecolor='black',
                                        alpha=0.4)
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





    def grade(self)-> int:
        grade=0
        for shape in self.Shapes:
            grade+=shape.Value
        return grade
