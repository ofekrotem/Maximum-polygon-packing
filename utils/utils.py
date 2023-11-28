import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

VISUALIZE_SOLUTION = True
PLOT_OFFSET = 300

def load_json_from_file(file_path):
    absolute_path = os.path.dirname(__file__)
    file_path = os.path.join(absolute_path, file_path)
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None

def is_valid_solution(input_json, output_json):
    if input_json is None or output_json is None:
        print("Input or output file not found.")
        return False

    # Check type
    if output_json.get("type") != "cgshop2024_solution":
        print("Type is not cgshop2024_solution.")
        return False

    # Check instance name
    if output_json.get("instance_name") != input_json.get("instance_name"):
        print("Instance name does not match.")
        return False

    # Check valid indices
    num_items = input_json.get("num_items")
    item_indices = output_json.get("item_indices")
    if any(index < 0 or index >= num_items for index in item_indices):
        print("Item indices are not valid.")
        return False

    # Check translations
    num_included_items = output_json.get("num_included_items")
    x_translations = output_json.get("x_translations")
    y_translations = output_json.get("y_translations")
    if (
        len(item_indices) != num_included_items
        or len(x_translations) != num_included_items
        or len(y_translations) != num_included_items
    ):
        print("Number of translations does not match the number of included items.")
        return False

    # Check if items are inside the container and don't overlap
    container_x = input_json["container"]["x"]
    container_y = input_json["container"]["y"]

    for i in range(num_included_items):
        item_index = item_indices[i]
        x_translation = x_translations[i]
        y_translation = y_translations[i]

        item_x = [x + x_translation for x in input_json["items"][item_index]["x"]]
        item_y = [y + y_translation for y in input_json["items"][item_index]["y"]]

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
            other_x = [x + x_translations[j] for x in input_json["items"][other_index]["x"]]
            other_y = [y + y_translations[j] for y in input_json["items"][other_index]["y"]]

            if any(
                max(x1) > min(x2) and min(x1) < max(x2) and max(y1) > min(y2) and min(y1) < max(y2)
                for x1, y1 in zip([item_x], [item_y])
                for x2, y2 in zip([other_x], [other_y])
            ):
                print("Items overlap.")
                return False


    return True



def visualize_solution(container, items, item_indices, x_translations, y_translations):
    fig, ax = plt.subplots()

    # Plot the container
    container_polygon = patches.Polygon(list(zip(container['x'], container['y'])), closed=True, edgecolor='black', alpha=0.1)
    ax.add_patch(container_polygon)

    # Collect all coordinates for container and items
    all_x_coords = container['x']
    all_y_coords = container['y']

    for idx, translation in zip(item_indices, zip(x_translations, y_translations)):
        item = items[idx]
        x_translation, y_translation = translation

        item_x = [x + x_translation for x in item['x']]
        item_y = [y + y_translation for y in item['y']]

        all_x_coords.extend(item_x)
        all_y_coords.extend(item_y)

        item_polygon = patches.Polygon(list(zip(item_x, item_y)), closed=True, edgecolor='red', alpha=0.5)
        ax.add_patch(item_polygon)

        print(f"Item {idx} Coordinates: {item_x}, {item_y}")

    # Set plot limits based on all coordinates
    ax.set_xlim([min(all_x_coords) - PLOT_OFFSET, max(all_x_coords) + PLOT_OFFSET])
    ax.set_ylim([min(all_y_coords) - PLOT_OFFSET, max(all_y_coords) + PLOT_OFFSET])
    ax.set_aspect('equal', adjustable='box')  # Equal aspect ratio for x and y axes

    plt.show()






# Example usage:
input_json = load_json_from_file('../data/atris42.cgshop2024_instance.json')
print("Input instance:", input_json)
output_json = load_json_from_file('../data/artis42.cgshop2024_valid_solution.json')
print("Output solution:", output_json)
valid = is_valid_solution(input_json, output_json)
print("Is the solution valid?", valid)

if valid or VISUALIZE_SOLUTION:
    container = input_json["container"]
    items = input_json["items"]
    item_indices = output_json["item_indices"]
    x_translations = output_json["x_translations"]
    y_translations = output_json["y_translations"]

    visualize_solution(container, items, item_indices, x_translations, y_translations)