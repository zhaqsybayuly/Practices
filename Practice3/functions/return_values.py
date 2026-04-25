# How functions send results back

# Example 1: Returning a single number
def multiply(a, b):
    return a * b  # gives back the result

answer = multiply(4, 5)
print("4 x 5 =", answer)


# Example 2: Returning text
def make_greeting(name):
    message = "Welcome, " + name + "!"
    return message

greeting = make_greeting("Aibek")
print(greeting)


# Example 3: Returning a list
def get_even_numbers(numbers):
    # Make a new list for even numbers
    even_list = []
    for num in numbers:
        if num % 2 == 0:  # check if it's even
            even_list.append(num)
    return even_list  # send the list back

my_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
evens = get_even_numbers(my_numbers)
print("Even numbers:", evens)


# Example 4: Stopping early
def divide(a, b):
    # If b is 0, we stop and return an error message
    if b == 0:
        return "You can't divide by zero!"
    return a / b

print(divide(10, 2))
print(divide(10, 0))
