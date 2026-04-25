import os

# create nested directories with makedirs (mkdir can only make one level)
# exist_ok=True prevents an error if the folders are already there
os.makedirs("test_dir/subdir1/subdir2", exist_ok=True)
print("Created nested folders: test_dir/subdir1/subdir2")

# show the current working directory
print("Current working directory:", os.getcwd())

# list everything inside the current folder
print("\nContents of current folder:")
for item in os.listdir("."):
    print(" -", item)

# find files by extension (.py) in the current folder
print("\nPython files in this folder:")
for item in os.listdir("."):
    if item.endswith(".py"):
        print(" -", item)

# remove the empty inner directory
os.rmdir("test_dir/subdir1/subdir2")
print("\nRemoved test_dir/subdir1/subdir2")
