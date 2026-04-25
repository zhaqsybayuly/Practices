from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map() — apply a function to every element
# returns an iterator, so wrap with list() to print it
squared = list(map(lambda x: x * x, numbers))
print("Squared:", squared)

# filter() — keep only items that pass the condition
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

# reduce() — combine all items into a single value
total = reduce(lambda a, b: a + b, numbers)
print("Sum via reduce:", total)

# more reduce examples
product = reduce(lambda a, b: a * b, numbers)
print("Product:", product)

maximum = reduce(lambda a, b: a if a > b else b, numbers)
print("Max via reduce:", maximum)

# built-in aggregate functions for comparison
print("\nUsing built-ins:")
print("len:", len(numbers))
print("sum:", sum(numbers))
print("min:", min(numbers))
print("max:", max(numbers))
print("sorted descending:", sorted(numbers, reverse=True))
