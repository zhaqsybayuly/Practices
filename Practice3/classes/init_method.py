# __init__ is the "constructor". It runs when you create an object

# Example 1: Using __init__ to set up data
class Student:
    def __init__(self, name, grade):
        # Save name and grade for this specific student
        self.name = name
        self.grade = grade
        print(f"New student joined: {self.name}")

# These lines automatically run the __init__ function
student1 = Student("Aibek", 10)
student2 = Student("Dana", 11)


# Example 2: Using default values
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance  # if not told, starts at 0

    def show_balance(self):
        print(f"{self.owner}'s balance: ${self.balance}")


account1 = BankAccount("Aibek")        # uses 0
account2 = BankAccount("Dana", 500)    # uses 500

account1.show_balance()
account2.show_balance()


# Example 3: Doing math inside __init__
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Find the area right away
        self.area = width * height

    def describe(self):
        print(f"Rectangle: {self.width}x{self.height}, Area: {self.area}")


rect = Rectangle(5, 3)
rect.describe()
