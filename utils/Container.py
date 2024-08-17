from shapely import Polygon

class Container:
    """
    A class representing a container, defined by a series of coordinates.

    Attributes:
        X_cor (list[int]): List of x-coordinates defining the container.
        Y_cor (list[int]): List of y-coordinates defining the container.
        Instance_Name (str): The name of the instance for identification.
    """

    def __init__(self, x_cor: list[int] = [], y_cor: list[int] = [], in_name: str = ""):
        """
        Initializes the Container class with x and y coordinates and an optional instance name.

        Args:
            x_cor (list[int]): List of x-coordinates defining the container.
            y_cor (list[int]): List of y-coordinates defining the container.
            in_name (str): Optional name of the instance for identification.

        Raises:
            Exception: If the length of x_cor and y_cor do not match.
        """
        if len(x_cor) != len(y_cor):
            raise Exception("Unmatched sizes!")
        self.X_cor = x_cor
        self.Y_cor = y_cor
        self.Instance_Name = in_name

    def __str__(self):
        """
        Returns a string representation of the container.

        Returns:
            str: A string representing the container's instance name and coordinates.
        """
        str_representation = f"Instance Name: {self.Instance_Name}\n"
        for i in range(len(self.X_cor)):
            str_representation += f"({self.X_cor[i]} , {self.Y_cor[i]})\n"
        return str_representation

    def export_to_json(self):
        """
        Serializes the container object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary containing the container's x and y coordinates and instance name.
        """
        json_data = {
            "container": {
                "x": self.X_cor,
                "y": self.Y_cor
            },
            "instance_name": self.Instance_Name
        }
        return json_data

    def get_polygon_object(self):
        """
        Creates a Shapely Polygon object representing the container.

        Returns:
            Polygon: A Shapely Polygon object representing the container based on its coordinates.
        """
        return Polygon(list(zip(self.X_cor, self.Y_cor)))

    def get_area(self):
        """
        Calculates the area of the container using its polygon representation.

        Returns:
            float: The area of the container.
        """
        return self.get_polygon_object().area
