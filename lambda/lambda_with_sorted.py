# sorted() organizes a list, and lambda tells it HOW to do it

# Example 1: Simple sorting
numbers = [5, 2, 8, 1, 9, 3]

# Sorting from smallest to biggest
sorted_numbers = sorted(numbers)
print("Up:", sorted_numbers)

# Sorting from biggest to smallest
sorted_desc = sorted(numbers, reverse=True)
print("Down:", sorted_desc)


# Example 2: Sorting by word length
words = ["banana", "apple", "kiwi", "strawberry", "fig"]

# Tell Python to look at the length (len) to sort
sorted_by_length = sorted(words, key=lambda word: len(word))

print("By length:", sorted_by_length)


# Example 3: Sorting tuples (pairs of data)
students = [("Aibek", 85), ("Dana", 92), ("Marat", 78), ("Zara", 95)]

# Sort by the score (which is at index 1)
sorted_by_score = sorted(students, key=lambda student: student[1])

print("By score:")
for name, score in sorted_by_score:
    print(f"  {name}: {score}")


# Example 4: Sorting a list of dictionaries
people = [
    {"name": "Aibek", "age": 22},
    {"name": "Dana", "age": 19},
    {"name": "Marat", "age": 25},
]

# Sort by the "age" key
sorted_by_age = sorted(people, key=lambda person: person["age"])

print("By age:")
for person in sorted_by_age:
    print(f"  {person['name']} is {person['age']}")
