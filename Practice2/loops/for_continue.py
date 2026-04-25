# continue skips the current iteration and goes to the next item
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue   # don't print banana
    print(x)

# skip even numbers
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)
