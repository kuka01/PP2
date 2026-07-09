import os

# Create directory

os.mkdir("Folder1")

# Create nested directories

os.makedirs("Folder2/SubFolder", exist_ok=True)

print("Directories created")

# Current directory

print(os.getcwd())

# List files

print(os.listdir())