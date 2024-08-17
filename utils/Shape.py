from shapely.geometry import Polygon

class Shape:
    """
    A class representing a geometric shape, defined by a series of coordinates, quantity, value, and an index.

    Attributes:
        X_cor (list[int]): List of x-coordinates defining the shape.
        Y_cor (list[int]): List of y-coordinates defining the shape.
        Quantity (int): The quantity of this shape.
        real_value (int): The real value of the shape.
        X_offset (int): The x-offset applied to the shape.
        Y_offset (int): The y-offset applied to the shape.
        Value (int): The calculated value of the shape, considering its area.
        Index (int): The original index of the shape in the instance file.
    """

    def __init__(self, x_cor: list[int], y_cor: list[int], qnty: int, val: int, index: int):
        """
        Initializes the Shape class with x and y coordinates, quantity, value, and index.

        Args:
            x_cor (list[int]): List of x-coordinates defining the shape.
            y_cor (list[int]): List of y-coordinates defining the shape.
            qnty (int): The quantity of this shape.
            val (int): The real value of the shape.
            index (int): The original index of the shape in the instance file.

        Raises:
            Exception: If the length of x_cor and y_cor do not match.
        """
        if len(x_cor) != len(y_cor):
            raise Exception("Unmatched sizes!")
        self.X_cor = x_cor
        self.Y_cor = y_cor
        self.Quantity = qnty
        self.real_value = val
        self.X_offset = 0
        self.Y_offset = 0
        self.Value = self.calculated_value()
        self.Index = index

    def calculated_value(self) -> int:
        """
        Calculates the value of the shape based on its real value and area.

        Returns:
            int: The calculated value of the shape.
        """
        area = self.get_area()
        return self.real_value / area

    def __str__(self):
        """
        Returns a string representation of the shape, including its value, quantity, coordinates, and index.

        Returns:
            str: A string representing the shape's details.
        """
        str_representation = f"Value: {self.real_value} \n Quantity: {self.Quantity} \n"
        for i in range(len(self.X_cor)):
            str_representation += f"({self.X_cor[i] + self.X_offset} , {self.Y_cor[i] + self.Y_offset})\n"
        str_representation += f"Original Index in instance file: {self.Index}"
        return str_representation

    def get_area(self) -> float:
        """
        Calculates the area of the shape using its polygon representation.

        Returns:
            float: The area of the shape.
        """
        poly = self.create_polygon_object()
        return poly.area

    def get_perimeter(self) -> float:
        """
        Calculates the perimeter of the shape using its polygon representation.

        Returns:
            float: The perimeter of the shape.
        """
        poly = self.create_polygon_object()
        return poly.length

    def get_real_coords(self) -> list[int]:
        """
        Returns the real coordinates of the shape, considering any applied offsets.

        Returns:
            list[int]: Two lists containing the real x and y coordinates of the shape.
        """
        real_x = [x + self.X_offset for x in self.X_cor]
        real_y = [y + self.Y_offset for y in self.Y_cor]
        return real_x, real_y

    def create_polygon_object(self) -> Polygon:
        """
        Creates a Shapely Polygon object representing the shape.

        Returns:
            Polygon: A Shapely Polygon object representing the shape based on its real coordinates.
        """
        real_x, real_y = self.get_real_coords()
        return Polygon(list(zip(real_x, real_y)))
