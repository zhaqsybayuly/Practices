# comparison operators always return a boolean
a = 200
b = 33

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# you can also store the comparison result in a variable
result = (a == b)
print(result)   # False

# common comparison operators
print(5 == 5)   # equal
print(5 != 4)   # not equal
print(5 >= 5)   # greater than or equal
print(5 <= 4)   # less than or equal
