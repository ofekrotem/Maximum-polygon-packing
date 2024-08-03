from shapely.geometry import Polygon


class Shape:
    def __init__(self, x_cor:list[int], y_cor:list[int], qnty:int, val:int, index:int):
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


    def calculated_value(self)->int:
        area = self.get_area()
        return self.real_value / area

    def __str__(self):
        str = f"Value: {self.Value} \n Quantity: {self.Quantity} \n"
        for i in range(len(self.X_cor)):
            str += f"({self.X_cor[i] + self.X_offset} , {self.Y_cor[i] + self.Y_offset})\n"
        str += f"Original Index in instance file: {self.Index}"
        return str

    def get_area(self)->float:
        poly = self.create_polygon_object()
        return poly.area

    def get_perimeter(self)->float:
        poly = self.create_polygon_object()
        return poly.length

    def get_real_coords(self)->list[int]:
        real_x = [x + self.X_offset for x in self.X_cor]
        real_y = [y + self.Y_offset for y in self.Y_cor]
        return real_x, real_y

    def create_polygon_object(self)->list[(int,int)]:
        real_x, real_y = self.get_real_coords()
        return Polygon(list(zip(real_x, real_y)))


