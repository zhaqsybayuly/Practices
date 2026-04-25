# A class can learn things from more than one parent!

# Example 1: Basic multiple inheritance
class Flyable:
    def fly(self):
        print(f"{self.name} is flying through the air!")


class Swimmable:
    def swim(self):
        print(f"{self.name} is swimming in the water!")


# Duck can do both! It inherits from both parents.
class Duck(Flyable, Swimmable):
    def __init__(self, name):
        self.name = name

    def quack(self):
        print(f"{self.name} says: Quack!")


donald = Duck("Donald")
donald.fly()    # from Flyable parent
donald.swim()   # from Swimmable parent
donald.quack()  # from Duck itself


# Example 2: A student who also works
class Worker:
    def work(self):
        print(f"{self.name} is at work.")


class Student:
    def study(self):
        print(f"{self.name} is studying for a test.")


# This class combines both
class WorkingStudent(Worker, Student):
    def __init__(self, name):
        self.name = name


person = WorkingStudent("Aibek")
person.work()   # from Worker parent
person.study()  # from Student parent
print(f"{person.name} is busy!")
