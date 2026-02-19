# Lambda is just a one-line function without a name

# Example 1: Regular function vs Lambda
# This is a normal function
def square_regular(x):
    return x * x

# This is a lambda doing the same thing
square_lambda = lambda x: x * x

print(square_regular(5))
print(square_lambda(5))


# Example 2: Lambda with two inputs
# A lambda that adds two numbers together
add = lambda a, b: a + b

print(add(3, 7))
print(add(10, 20))


# Example 3: Checking a condition
# Returns True if the number is even
is_even = lambda num: num % 2 == 0

print(is_even(4))
print(is_even(7))


# Example 4: Using strings
# A lambda that creates a hello message
make_hello = lambda name: "Hello, " + name + "!"

print(make_hello("Aibek"))
print(make_hello("Dana"))
