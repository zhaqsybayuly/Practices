# Learning how to use *args and **kwargs

# Example 1: *args - takes many numbers
# The * means we can pass as many values as we want
# They get stored in a tuple called "args"
def add_all(*args):
    total = 0
    for number in args:
        total += number
    return total

print(add_all(1, 2))           # 2 numbers
print(add_all(1, 2, 3, 4, 5)) # 5 numbers
print(add_all(10))             # just 1 number


# Example 2: *args with a normal argument
# We can put a regular argument first, then *args
def greet_many(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet_many("Hello", "Aibek", "Dana", "Marat")


# Example 3: **kwargs - takes named arguments
# The ** collects things like name="Aibek" into a dictionary
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_info(name="Aibek", age=20, city="Almaty")


# Example 4: Using both *args and **kwargs
# We can use both in one function to grab everything
def describe(*args, **kwargs):
    print("List of things:", args)
    print("Extra details:", kwargs)

describe("apple", "banana", color="red", count=3)
