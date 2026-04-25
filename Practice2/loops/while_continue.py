# continue skips the current iteration and moves on to the next
i = 0
while i < 6:
    i += 1
    if i == 3:
        continue   # skip printing 3
    print(i)

# print only odd numbers from 1 to 10
n = 0
while n < 10:
    n += 1
    if n % 2 == 0:
        continue
    print(n)
