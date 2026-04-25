# the three boolean operators: and, or, not
x = 5
y = 10

# AND — both conditions must be True
print(x > 0 and y > 0)    # True

# OR — at least one condition must be True
print(x > 100 or y > 0)   # True

# NOT — flips True to False and vice versa
print(not (x == y))       # True (because x != y)

# combining operators
age = 20
has_id = True
if age >= 18 and has_id:
    print("Allowed in")
