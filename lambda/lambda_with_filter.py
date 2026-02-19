# filter() helps us pick only the items we want from a list

# Example 1: Getting only even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# filter(rule, list) - keeps items if they follow the rule
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print("Full list:", numbers)
print("Only evens:", even_numbers)


# Example 2: Numbers bigger than 5
big_numbers = list(filter(lambda x: x > 5, numbers))
print("Bigger than 5:", big_numbers)


# Example 3: Finding long names
names = ["Ali", "Aibek", "Dana", "Nursultan", "Zara"]

# Pick names with more than 4 letters
long_names = list(filter(lambda name: len(name) > 4, names))

print("All names:", names)
print("Long names:", long_names)


# Example 4: Removing negative numbers
mixed_numbers = [-5, -3, 0, 2, 4, -1, 7, 9]

# Keep only those greater than 0
positive_only = list(filter(lambda x: x > 0, mixed_numbers))

print("Mixed list:", mixed_numbers)
print("Only positive:", positive_only)
