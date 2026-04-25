# Overriding means the child class replaces a parent's method with its own

# Example 1: Overriding the speak() method
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a noise.")


class Dog(Animal):
    # Dog has its own special version of speak
    def speak(self):
        print(f"{self.name} says: Woof!")


class Cat(Animal):
    # Cat also has its own version of speak
    def speak(self):
        print(f"{self.name} says: Meow!")


class Bird(Animal):
    # Bird doesn't have a special version, so it uses the Parent's version
    pass


animals = [Dog("Rex"), Cat("Whiskers"), Bird("Tweety")]

# Each one uses its own version of speak()
for animal in animals:
    animal.speak()


# Example 2: Changing how an object looks when printed
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    # This replaces the default print behavior
    def __str__(self):
        return f'"{self.title}" by {self.author}'


book = Book("Python Basics", "Aibek")
print(book)  # Uses our custom string description
