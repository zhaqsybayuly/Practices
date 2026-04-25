# Different ways to send data to functions

# Example 1: Arguments in order
# The order we send things matters here
def describe_pet(animal_type, pet_name):
    print(f"I have a {animal_type} and its name is {pet_name}.")

describe_pet("dog", "Rex")
describe_pet("cat", "Whiskers")


# Example 2: Using names for arguments
# If we use names, the order doesn't matter
def make_pizza(size, crust, topping):
    print(f"Making a {size} pizza with {crust} crust and {topping}.")

make_pizza(topping="cheese", size="large", crust="thin")


# Example 3: Default values
# If we don't send a value, it uses the default one
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Aibek")              # uses "Hello"
greet("Dana", "Hi there")    # uses "Hi there"


# Example 4: Sending a list
# We can send a whole list of things to a function
def print_all_fruits(fruits_list):
    print("Printing the list:")
    for fruit in fruits_list:
        print(" -", fruit)

my_fruits = ["apple", "banana", "mango"]
print_all_fruits(my_fruits)
