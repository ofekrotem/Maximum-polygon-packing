import json
from matplotlib import pyplot as plt, patches
from shapely.geometry import Polygon
from .Container import Container
from .Shape import Shape

PLOT_OFFSET = 300


class Solution:
    def __init__(self, type: str, name: str, meta: dict[str:str], items: list[int], x: list[int], y: list[int],
                 cont: Container, shapes: list[Shape]):
        if len(items) != len(x) != len(y):
            raise Exception("Unmatched Sizes!")
        self.Type = type
        self.Name = name
        self.Meta = meta
        self.Items_ID = items
        self.X_Offset = x
        self.Y_Offset = y
        self.Container = cont
        self.Shapes = shapes

    def __str__(self):
        str = f"Selected {len(self.Y_Offset)} shapes.\n"
        for i in range(len(self.Y_Offset)):
            str += f"Shape {i + 1} (ID: {self.Items_ID[i]}):\n \t X offset: {self.X_Offset[i]}\n \t Y offset: {self.Y_Offset[i]}\n"
        return str

    def export_to_json(self) -> json:
        json_data = {
            "type": self.Type,
            "instance_name": self.Name,
            "num_included_items": len(self.Items_ID),
            "meta": self.Meta,
            "item_indices": self.Items_ID,
            "x_translations": self.X_Offset,
            "y_translations": self.Y_Offset
        }
        return json_data

    def is_valid(self) -> bool:
        if any(index < 0 or index >= len(self.Shapes) for index in self.Items_ID):
            return False

        # Create a list of Shapely Polygons for each shape
        shape_polygons = [Polygon([(x + self.X_Offset[i], y + self.Y_Offset[i]) for x, y in zip(
            self.Shapes[item_index].X_cor, self.Shapes[item_index].Y_cor)]) for i, item_index in enumerate(self.Items_ID)]

        for i in range(len(shape_polygons)):
            for j in range(i + 1, len(shape_polygons)):
                if shape_polygons[i].intersects(shape_polygons[j]):
                    return False

        # Check if all shapes are inside the container
        container_polygon = Polygon(list(zip(self.Container.X_cor, self.Container.Y_cor)))
        for i in range(len(shape_polygons)):
            if not container_polygon.contains(shape_polygons[i]):
                return False

        return True

    def visualize_solution(self) -> None:
        fig, ax = plt.subplots()

        ax.text(0.5, 1.05, f"Value:{self.grade()} ", horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, fontweight='bold')

        # Plot the container
        container_polygon = patches.Polygon(list(zip(self.Container.X_cor, self.Container.Y_cor)), closed=True,
                                            edgecolor='black',
                                            alpha=0.4)
        ax.add_patch(container_polygon)

        # Collect all coordinates for container and items
        all_x_coords = self.Container.X_cor
        all_y_coords = self.Container.Y_cor

        for idx, translation in zip(self.Items_ID, zip(self.X_Offset, self.Y_Offset)):
            item = self.Shapes[idx]
            x_translation, y_translation = translation

            item_x = [x + x_translation for x in item.X_cor]
            item_y = [y + y_translation for y in item.Y_cor]

            all_x_coords.extend(item_x)
            all_y_coords.extend(item_y)

            item_polygon = patches.Polygon(list(zip(item_x, item_y)), closed=True, edgecolor='red', alpha=0.5)
            ax.add_patch(item_polygon)

        # Set plot limits based on all coordinates
        ax.set_xlim([min(all_x_coords) - PLOT_OFFSET, max(all_x_coords) + PLOT_OFFSET])
        ax.set_ylim([min(all_y_coords) - PLOT_OFFSET, max(all_y_coords) + PLOT_OFFSET])
        ax.set_aspect('equal', adjustable='box')  # Equal aspect ratio for x and y axes

        plt.show()

    def grade(self)-> int:
        grade=0
        for index in self.Items_ID:
            grade=grade+self.Shapes[index].Value
        return grade

    @classmethod
    def import_from_json(cls, json_data):
        type = json_data.get("type", "")
        name = json_data.get("instance_name", "")
        meta = json_data.get("meta", {})
        items = json_data.get("item_indices", [])
        x = json_data.get("x_translations", [])
        y = json_data.get("y_translations", [])

        sol = Solution(type, name, meta, items, x, y, Container(), [])

        return sol
