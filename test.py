class Parent:
    def __init__(self, x):
        self.x = x
    def func():
        pass

class Child(Parent):
    def __init__(self, x):
        # super().__init__(x)
        pass

b = Child("a")
b.func()