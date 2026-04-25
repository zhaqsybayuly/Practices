# Task 1: generator that yields squares of numbers up to N
def squares_up_to(n):
    for i in range(1, n + 1):
        yield i * i

print("Task 1 — squares up to 5:")
for sq in squares_up_to(5):
    print(sq)

# Task 2: print even numbers from 0 to n in comma-separated form
def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i

n = int(input("\nTask 2 — enter n: "))
print(",".join(str(x) for x in even_numbers(n)))

# Task 3: numbers divisible by 3 AND 4 between 0 and n
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print("\nTask 3 — divisible by 3 and 4 up to 50:")
for x in divisible_by_3_and_4(50):
    print(x, end=" ")
print()

# Task 4: squares from a to b (inclusive)
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

print("\nTask 4 — squares from 2 to 6:")
for s in squares(2, 6):
    print(s)

# Task 5: numbers from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

print("\nTask 5 — countdown from 5:")
for x in countdown(5):
    print(x, end=" ")
print()
