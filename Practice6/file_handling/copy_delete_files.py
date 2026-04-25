import shutil
import os

# make a backup copy of sample.txt
shutil.copy("sample.txt", "sample_backup.txt")
print("File copied to sample_backup.txt")

# safely delete the backup if it exists
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("sample_backup.txt was deleted")
else:
    print("Backup file does not exist")
