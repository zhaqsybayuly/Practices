import math

# Task 1: convert degree to radian
degree = float(input("Task 1 — input degree: "))
radian = degree * math.pi / 180
print(f"Output radian: {radian:.6f}")

# Task 2: area of a trapezoid
height = float(input("\nTask 2 — Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
trapezoid_area = (base1 + base2) / 2 * height
print(f"Expected Output: {trapezoid_area}")

# Task 3: area of a regular polygon
sides = int(input("\nTask 3 — input number of sides: "))
length = float(input("Input the length of a side: "))
polygon_area = (sides * length ** 2) / (4 * math.tan(math.pi / sides))
print(f"The area of the polygon is: {polygon_area}")

# Task 4: area of a parallelogram
base = float(input("\nTask 4 — Length of base: "))
height = float(input("Height of parallelogram: "))
parallelogram_area = base * height
print(f"Expected Output: {parallelogram_area}")
