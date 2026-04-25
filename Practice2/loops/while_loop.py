# while loop: keeps running while the condition is True
i = 1
while i < 6:
    print(i)
    i += 1   # important — without this we get an infinite loop

# countdown example
n = 5
while n > 0:
    print(n)
    n -= 1
print("Done!")
