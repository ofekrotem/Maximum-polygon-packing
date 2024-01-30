import json


class Solution:
    def __init__(self, type, name, num, meta, items, x, y):
        if len(items) != len(x) or len(x) != len(y):
            raise Exception("Unmatched Sizes!")
        self.Type = type
        self.Name = name
        self.Items_Num = num
        self.Meta = meta
        self.Items_ID = items
        self.X_Offset = x
        self.Y_Offset = y

    def __str__(self):
        output = f"Selected {len(self.Y_Offset)} shapes.\n"
        for i in range(len(self.Y_Offset)):
            output += f"Shape {i+1} (ID: {self.Items_ID[i]}):\n \t X offset: {self.X_Offset[i]}\n \t Y offset: {self.Y_Offset[i]}\n"
        return output

    def export_to_json(self):
        json_data = {
            "type": self.Type,
            "instance_name": self.Name,
            "num_included_items": self.Items_Num,
            "meta": self.Meta,
            "item_indices": self.Items_ID,
            "x_translations": self.X_Offset,
            "y_translations": self.Y_Offset
        }
        return json.dumps(json_data)

    def __iter__(self):
        return iter(zip(self.Items_ID, self.X_Offset, self.Y_Offset))