class Container:
    def __init__(self,x_cor:list[int]=[],y_cor:list[int]=[],in_name:str=""):
        if len(x_cor) != len(y_cor):
            raise Exception("Unmatched sizes!")
        self.X_cor=x_cor
        self.Y_cor=y_cor
        self.Instance_Name=in_name

    def __str__(self):
        str=f"Instance Name: {self.Instance_Name}\n"
        for i in range(len(self.X_cor)):
            str+=f"({self.X_cor[i]} , {self.Y_cor[i]})\n"
        return str
