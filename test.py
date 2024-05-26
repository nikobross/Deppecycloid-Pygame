class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.list = [self.x, self.y]
    
    def change_xy(self, x, y):
        self.x = x
        self.y = y

    def __str__ (self):
        string = str(self.x) + " " + str(self.y)
        return string



car1 = Car(10, 10)

car1.change_xy(20, 20)

print(car1.list)

print(car1.x, car1.y)