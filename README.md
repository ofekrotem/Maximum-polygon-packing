# Maximum-polygon-packing

Each instance consists of a simple convex container polygon (container) and a list of simple packable polygon items (items).
It also contains some general information, such as the instance name (instance_name), the number of different items (num_items), and some additional information for internal analysis and evaluation (meta).

Polygons are encoded by their points in two lists for x and y coordinates. These points are on a large integer grid and listed in a counter-clockwise orientation without a closing point.
In addition to the list, each item in the list of items also has an individual value you can gain by packing it, and a quantity indicating how often you can use this item.

## Solution Format Specifications
You can submit zip-archives, containing any amount of your solutions. Each solution is stored in an individual JSON file containing a single dict.   There's an example below, but these are the specified fields in the diet:

