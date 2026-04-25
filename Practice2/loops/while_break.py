# break stops the loop immediately, even if the condition is still True
i = 1
while i < 6:
    print(i)
    if i == 3:
        break    # exit the loop when i reaches 3
    i += 1

# searching for a value
numbers = [1, 5, 9, 3, 7]
target = 9
i = 0
while i < len(numbers):
    if numbers[i] == target:
        print(f"Found at index {i}")
        break
    i += 1
