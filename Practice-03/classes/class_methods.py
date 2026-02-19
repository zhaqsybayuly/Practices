# Methods are just functions that belong to a class

# Example 1: Methods in a Circle class
class Circle:
    def __init__(self, radius):
        self.radius = radius

    # A method to find the area
    def get_area(self):
        area = 3.14159 * self.radius ** 2
        return area

    # A method to find the circumference (length around)
    def get_circumference(self):
        return 2 * 3.14159 * self.radius

    # A method that prints all the info
    def describe(self):
        print(f"Circle with radius {self.radius}")
        print(f"  Area: {self.get_area():.2f}")
        print(f"  Circumference: {self.get_circumference():.2f}")


c = Circle(5)
c.describe()


# Example 2: Methods that change the object
class Counter:
    def __init__(self):
        self.count = 0  # start at 0

    def increase(self):
        self.count += 1  # add one

    def decrease(self):
        self.count -= 1  # take away one

    def reset(self):
        self.count = 0   # go back to 0

    def show(self):
        print(f"Current count: {self.count}")


counter = Counter()
counter.show()
counter.increase()
counter.increase()
counter.show()
counter.decrease()
counter.show()
counter.reset()
counter.show()
