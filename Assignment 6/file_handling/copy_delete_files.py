import shutil
import os

# Copy file

shutil.copy("sample.txt", "backup.txt")

print("backup.txt created")

# Delete backup

if os.path.exists("backup.txt"):
    os.remove("backup.txt")
    print("backup.txt deleted")
else:
    print("File not found")