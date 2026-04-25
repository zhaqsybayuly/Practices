# short-hand if: write a single-line if when there is only one statement
a = 200
b = 33

if a > b: print("a is greater than b")

# short-hand if/else (also called the ternary expression)
a = 2
b = 330
print("A") if a > b else print("B")

# you can also assign the result of a ternary expression to a variable
age = 18
status = "adult" if age >= 18 else "minor"
print(status)
