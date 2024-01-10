import json
import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt

from Container import Container
from Shape import Shape
from Soultion import Solution

VISUALIZE_SOLUTION = True
PLOT_OFFSET = 300


def load_json_from_file(file_path,classification):
    absolute_path = os.path.dirname(__file__)
    file_path = os.path.join(absolute_path, file_path)
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            if(classification=='i'):
                shapes_data = json_data['items']
                shapes_list=[]
                cont = Container(json_data['container']['x'], json_data['container']['y'],json_data['instance_name'])
                for item in shapes_data:
                    shapes_list.append(Shape(item['x'],item['y'],item['quantity'],item['value']))
                return (cont,shapes_list)
            else:
                sol= Solution(json_data['type'],json_data['instance_name'],json_data['num_included_items'],json_data['meta'],json_data['item_indices'],json_data['x_translations'],json_data['y_translations'])
                return sol
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None


def is_valid_solution(container, shapes, solution):
    if container is None or shapes is None or solution is None:
        print("Problems with Objects build!!")
        return False

    # Check type
    if solution.Type != "cgshop2024_solution":
        print("Type is not cgshop2024_solution.")
        return False

    # Check instance name
    if solution.Name != container.Instance_Name:
        print("Instance name does not match.")
        return False

    # Check valid indices
    num_items = len(shapes)
    item_indices = solution.Items_ID
    if any(index < 0 or index >= num_items for index in item_indices):
        print("Item indices are not valid.")
        return False

    # Check translations
    num_included_items = solution.Items_Num
    x_translations = solution.X_Offset
    y_translations = solution.Y_Offset
    if (
            len(item_indices) != num_included_items
            or len(x_translations) != num_included_items
            or len(y_translations) != num_included_items
    ):
        print("Number of translations does not match the number of included items.")
        return False

    # Check if items are inside the container and don't overlap
    container_x = container.X_cor
    container_y = container.Y_cor

    for i in range(num_included_items):
        item_index = item_indices[i]
        x_translation = x_translations[i]
        y_translation = y_translations[i]

        item_x = [x + x_translation for x in shapes[item_index].X_cor]
        item_y = [y + y_translation for y in shapes[item_index].Y_cor]

        # Check if item is inside the container
        if any(
                x < min(container_x) or x > max(container_x) or y < min(container_y) or y > max(container_y)
                for x, y in zip(item_x, item_y)
        ):
            print("Item is not inside the container.")
            return False

        # Check for item overlap
        for j in range(i + 1, num_included_items):
            other_index = item_indices[j]
            other_x = [x + x_translations[j] for x in shapes[other_index].X_cor]
            other_y = [y + y_translations[j] for y in shapes[other_index].Y_cor]

            if any(
                    max(x1) > min(x2) and min(x1) < max(x2) and max(y1) > min(y2) and min(y1) < max(y2)
                    for x1, y1 in zip([item_x], [item_y])
                    for x2, y2 in zip([other_x], [other_y])
            ):
                print("Items overlap.")
                return False

    return True


def visualize_solution(container, shapes,solution):
    fig, ax = plt.subplots()

    # Plot the container
    container_polygon = patches.Polygon(list(zip(container.X_cor, container.Y_cor)), closed=True, edgecolor='black',
                                        alpha=0.1)
    ax.add_patch(container_polygon)

    # Collect all coordinates for container and items
    all_x_coords = container.X_cor
    all_y_coords = container.Y_cor

    for idx, translation in zip(solution.Items_ID, zip(solution.X_Offset, solution.Y_Offset)):
        item = shapes[idx]
        x_translation, y_translation = translation

        item_x = [x + x_translation for x in item.X_cor]
        item_y = [y + y_translation for y in item.Y_cor]

        all_x_coords.extend(item_x)
        all_y_coords.extend(item_y)

        item_polygon = patches.Polygon(list(zip(item_x, item_y)), closed=True, edgecolor='red', alpha=0.5)
        ax.add_patch(item_polygon)

        #print(f"Item {idx} Coordinates: {item_x}, {item_y}")

    # Set plot limits based on all coordinates
    ax.set_xlim([min(all_x_coords) - PLOT_OFFSET, max(all_x_coords) + PLOT_OFFSET])
    ax.set_ylim([min(all_y_coords) - PLOT_OFFSET, max(all_y_coords) + PLOT_OFFSET])
    ax.set_aspect('equal', adjustable='box')  # Equal aspect ratio for x and y axes

    plt.show()

# Example usage:
CONTAINER,SHAPES_LIST = load_json_from_file('../data/atris42.cgshop2024_instance.json','i')
SOLUTION = load_json_from_file('../data/artis42.cgshop2024_items_overlap_solution.json','s')
valid = is_valid_solution(CONTAINER,SHAPES_LIST,SOLUTION)
print("Is the solution valid?", valid)

if valid or VISUALIZE_SOLUTION:
    visualize_solution(CONTAINER, SHAPES_LIST, SOLUTION)
