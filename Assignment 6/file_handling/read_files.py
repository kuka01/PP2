# Read entire file

with open("sample.txt", "r") as file:
    print(file.read())

print()

# Read first line

with open("sample.txt", "r") as file:
    print(file.readline())

print()

# Read all lines

with open("sample.txt", "r") as file:
    print(file.readlines())