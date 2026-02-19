# super() is used to call functions from the Parent class

# Example 1: Using super() to set up data
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f"Person {self.name} is ready.")

    def introduce(self):
        print(f"Hi, I am {self.name} and I am {self.age}.")


class Student(Person):
    def __init__(self, name, age, student_id):
        # Use the Parent (Person) to set up name and age
        super().__init__(name, age)
        # Then add the stuff only students have
        self.student_id = student_id
        print(f"ID set to: {self.student_id}")

    def study(self):
        print(f"{self.name} is hitting the books!")


s = Student("Aibek", 20, "S999")
s.introduce()  # from Person parent
s.study()      # from Student child


# Example 2: Using super() to add onto a method
class Shape:
    def describe(self):
        print("This is a shape.")


class ColoredShape(Shape):
    def __init__(self, color):
        self.color = color

    def describe(self):
        # Run the Parent's describe first
        super().describe()
        # Then add our extra information
        print(f"And its color is {self.color}.")


cs = ColoredShape("blue")
cs.describe()
