import json

from matplotlib import pyplot as plt, patches

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
        return json.dumps(json_data)

    def is_valid(self) -> bool:
        if any(index < 0 or index >= len(self.Items_ID) for index in self.Items_ID):
            return False

        for i in range(len(self.Items_ID)):
            item_index = self.Items_ID[i]
            x_translation = self.X_Offset[i]
            y_translation = self.Y_Offset[i]

            item_x = [x + x_translation for x in self.Shapes[item_index].X_cor]
            item_y = [y + y_translation for y in self.Shapes[item_index].Y_cor]

            # Check if item is inside the container
            if any(
                    x < min(self.Container.X_cor) or x > max(self.Container.X_cor) or y < min(
                        self.Container.Y_cor) or y > max(
                        self.Container.Y_cor)
                    for x, y in zip(item_x, item_y)
            ):
                return False

            # Check for item overlap
            for j in range(i + 1, len(self.Items_ID)):
                other_index = self.Items_ID[j]
                other_x = [x + self.X_Offset[j] for x in self.Shapes[other_index].X_cor]
                other_y = [y + self.Y_Offset[j] for y in self.Shapes[other_index].Y_cor]

                if any(
                        max(x1) > min(x2) and min(x1) < max(x2) and max(y1) > min(y2) and min(y1) < max(y2)
                        for x1, y1 in zip([item_x], [item_y])
                        for x2, y2 in zip([other_x], [other_y])
                ):
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
