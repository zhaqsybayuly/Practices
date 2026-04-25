# create a text file and write sample data into it
# 'w' mode creates the file if it doesn't exist, or overwrites it if it does
with open("sample.txt", "w") as f:
    f.write("Hello, this is line 1\n")
    f.write("This is line 2\n")
    f.write("Line 3 with some numbers: 42\n")

print("File 'sample.txt' was created with 3 lines.")

# append new lines to the same file using 'a' mode
# 'a' mode adds to the end without erasing existing content
with open("sample.txt", "a") as f:
    f.write("This line was appended\n")
    f.write("And one more appended line\n")

print("Appended 2 more lines to sample.txt")
