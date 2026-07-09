import shutil
import os

os.makedirs("Folder3", exist_ok=True)

if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "Folder3/sample.txt")

print("File copied to Folder3")