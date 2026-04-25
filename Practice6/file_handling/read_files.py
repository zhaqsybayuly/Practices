# read the whole file at once with read()
with open("sample.txt", "r") as f:
    content = f.read()
    print("=== read() output ===")
    print(content)

# read line by line with readline()
print("=== readline() output (first 2 lines) ===")
with open("sample.txt", "r") as f:
    print(f.readline(), end="")
    print(f.readline(), end="")

# read all lines into a list with readlines()
print("\n=== readlines() output ===")
with open("sample.txt", "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines, start=1):
        print(f"Line {i}: {line}", end="")
