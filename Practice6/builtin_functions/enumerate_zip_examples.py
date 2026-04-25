# enumerate() — gives both the index and the value while iterating
fruits = ["apple", "banana", "cherry"]
print("=== enumerate ===")
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip() — pair up items from two (or more) sequences
names = ["Arman", "Aruzhan", "Berik"]
ages = [20, 22, 19]
print("\n=== zip ===")
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# combine zip and enumerate
print("\n=== zip + enumerate ===")
for i, (name, age) in enumerate(zip(names, ages), start=1):
    print(f"{i}) {name} — {age}")

# type checking and conversion examples
print("\n=== type checks and conversions ===")
x = "42"
print("type of x:", type(x))
print("isinstance str:", isinstance(x, str))

# convert string → int → float → str again
n_int = int(x)
n_float = float(n_int)
n_str = str(n_float)
print(f"int: {n_int} ({type(n_int).__name__})")
print(f"float: {n_float} ({type(n_float).__name__})")
print(f"str: {n_str} ({type(n_str).__name__})")

# bool conversions
print("\nbool('') ->", bool(""))       # False
print("bool('hi') ->", bool("hi"))     # True
print("bool(0) ->", bool(0))           # False
print("bool(1) ->", bool(1))           # True
