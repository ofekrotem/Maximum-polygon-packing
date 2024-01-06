class Solution:
    def __init__(self,type,name,num,meta,items,x,y):
        if len(items)!=len(x)!=len(y):
            raise Exception("Unmatched Sizes!")
        self.Type=type
        self.Name=name
        self.Items_Num=num
        self.Meta=meta
        self.Items_ID=items
        self.X_Offset=x
        self.Y_Offset=y

    def __str__(self):
        str=f"Selected {len(self.Y_Offset)} shapes.\n"
        for i in range(len(self.Y_Offset)):
            str+=f"Shape {i+1} (ID: {self.Items_ID[i]}):\n \t X offset: {self.X_Offset[i]}\n \t Y offset: {self.Y_Offset[i]}\n"
        return str