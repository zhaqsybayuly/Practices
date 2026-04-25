# break exits the for loop early
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)
    if x == "banana":
        break    # stop after banana

# stop on first negative number
numbers = [3, 7, 2, -1, 5]
for n in numbers:
    if n < 0:
        print("Negative number found, stopping")
        break
    print(n)
