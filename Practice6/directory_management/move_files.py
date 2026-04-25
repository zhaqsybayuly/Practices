import os
import shutil
from pathlib import Path

# create source and destination folders
Path("source").mkdir(exist_ok=True)
Path("destination").mkdir(exist_ok=True)

# create a sample file in the source folder
with open("source/data.txt", "w") as f:
    f.write("Some data inside data.txt\n")

# copy the file from source to destination
shutil.copy("source/data.txt", "destination/data.txt")
print("File copied from source/ to destination/")

# move (rename) the copy to a new name in destination
shutil.move("destination/data.txt", "destination/data_moved.txt")
print("File moved/renamed inside destination/")

# print the final layout
print("\nsource/ contents:     ", os.listdir("source"))
print("destination/ contents:", os.listdir("destination"))
