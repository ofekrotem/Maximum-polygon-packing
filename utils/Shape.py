class Shape:
    def __init__(self, x_cor, y_cor,qty,val):
        if len(x_cor) != len(y_cor):
            raise Exception("Unmatched sizes!")
        self.X_cor = x_cor
        self.Y_cor = y_cor
        self.Quantity=qty
        self.Value=val

    def __str__(self):
        str=f"Value: {self.Value} \n Quantity: {self.Quantity} \n"
        for i in range(len(self.X_cor)):
            str += f"({self.X_cor[i]} , {self.Y_cor[i]})\n"
        return str
