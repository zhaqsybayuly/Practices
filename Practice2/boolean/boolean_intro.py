# booleans represent one of two values: True or False
print(10 > 9)    # True
print(10 == 9)   # False
print(10 < 9)    # False

# the bool() function evaluates any value to True or False
print(bool("Hello"))   # True — non-empty string
print(bool(15))        # True — non-zero number
print(bool(""))        # False — empty string
print(bool(0))         # False — zero
print(bool(None))      # False — None is always falsy
