# Inheritance lets a "child" class use code from a "parent" class

# Example 1: Basic inheritance
# This is the Parent class
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")

    def eat(self):
        print(f"{self.name} is eating.")


# Dog is the Child class. It copies everything from Animal!
class Dog(Animal):
    def fetch(self):
        print(f"{self.name} fetches the ball!")


class Cat(Animal):
    def purr(self):
        print(f"{self.name} is purring...")


# Dog and Cat get Animal's powers for free
dog = Dog("Rex")
cat = Cat("Whiskers")

dog.speak()   # works because it's an Animal
dog.eat()     # works because it's an Animal
dog.fetch()   # only works for Dog

cat.speak()   # works because it's an Animal
cat.purr()    # only works for Cat


# Example 2: Adding a custom __init__ to the child
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(f"{self.brand} is starting up...")


class ElectricCar(Vehicle):
    def __init__(self, brand, battery_size):
        # super().__init__ tells the Parent (Vehicle) to set up the brand
        super().__init__(brand)
        self.battery_size = battery_size

    def charge(self):
        print(f"{self.brand} is charging its {self.battery_size} kWh battery")


tesla = ElectricCar("Tesla", 100)
tesla.start()   # from Parent
tesla.charge()  # from Child
