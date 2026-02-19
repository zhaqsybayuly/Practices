# A class is like a blueprint for making objects

# Example 1: Making a simple Dog class
# We use "class" to define it
class Dog:
    # This is shared by all dogs
    species = "Canis familiaris"

    # This runs when we create a new dog
    def __init__(self, name, age):
        # These are unique for each dog
        self.name = name
        self.age = age

    # A function inside a class is called a method
    def bark(self):
        print(f"{self.name} says: Woof!")

    def describe(self):
        print(f"{self.name} is {self.age} years old.")


# Create two separate dog objects
dog1 = Dog("Rex", 3)
dog2 = Dog("Bella", 5)

# Use their methods
dog1.bark()
dog1.describe()
dog2.bark()
dog2.describe()

# Look at the shared variable
print("Species:", dog1.species)


# Example 2: A simple Car class
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def start_engine(self):
        print(f"{self.brand} {self.model} engine started!")

    def get_info(self):
        print(f"{self.year} {self.brand} {self.model}")


my_car = Car("Toyota", "Camry", 2022)
my_car.start_engine()
my_car.get_info()
