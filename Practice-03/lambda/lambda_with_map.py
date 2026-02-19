# map() runs a function on every item in a list

# Example 1: Doubling all numbers
numbers = [1, 2, 3, 4, 5]

# map(rule, list) - changes every item using the rule
doubled = list(map(lambda x: x * 2, numbers))

print("Before:", numbers)
print("After (doubled):", doubled)


# Example 2: Squaring all numbers
squared = list(map(lambda x: x ** 2, numbers))
print("Squared list:", squared)


# Example 3: Making text uppercase
names = ["aibek", "dana", "marat", "zara"]

# Change every name to big letters
upper_names = list(map(lambda name: name.upper(), names))

print("Small names:", names)
print("Big names:", upper_names)


# Example 4: Math on a whole list
# Changing Fahrenheit to Celsius for everyone
fahrenheit_temps = [32, 77, 95, 104]

celsius_temps = list(map(lambda f: round((f - 32) * 5 / 9, 1), fahrenheit_temps))

print("Fahrenheit:", fahrenheit_temps)
print("Celsius:", celsius_temps)
