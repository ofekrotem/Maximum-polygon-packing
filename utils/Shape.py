from shapely.geometry import Polygon


class Shape:
    def __init__(self, x_cor, y_cor, qnty, val, index):
        if len(x_cor) != len(y_cor):
            raise Exception("Unmatched sizes!")
        self.X_cor = x_cor
        self.Y_cor = y_cor
        self.Quantity = qnty
        self.Value = val
        self.Index = index
        self.Polygon = Polygon(self.create_polygon_object())

    def create_polygon_object(self):
        vertices = []
        for index in range(len(self.X_cor)):
            vertices.append((self.X_cor[index], self.Y_cor[index]))
        return vertices

    def __str__(self):

        str=f"Value: {self.Value} \n Quantity: {self.Quantity} \n";

        for i in range(len(self.X_cor)):
            str += f"({self.X_cor[i]} , {self.Y_cor[i]})\n"
        str += f"Original Index in instance file: {self.Index}"
        return str

    def get_area(self):
        return self.Polygon.area
