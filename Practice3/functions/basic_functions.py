# Making simple functions in Python

# Example 1: A function that just prints something
# We use "def" to start a function
def say_hello():
    print("Hello from the function!")

# Now we run it
say_hello()


# Example 2: A function that takes a name
# This function waits for a "name" to be sent to it
def greet_person(name):
    print("Hello, " + name + "!")

greet_person("Aibek")
greet_person("Dana")


# Example 3: A function that does math
# This one adds two numbers and gives the answer back
def add_numbers(a, b):
    result = a + b
    return result  # "return" sends the answer back

# Save the answer in a variable
total = add_numbers(10, 5)
print("10 + 5 =", total)


# Example 4: Adding a description (docstring)
def convert_to_celsius(fahrenheit):
    """
    This function changes Fahrenheit to Celsius.
    It takes a number and returns the new temperature.
    """
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius

temp_f = 77
temp_c = convert_to_celsius(temp_f)
print(f"{temp_f}F is {temp_c:.1f}C")
