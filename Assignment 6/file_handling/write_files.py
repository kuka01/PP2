# Create and write to a file

with open("sample.txt", "w") as file:
    file.write("Hello\n")
    file.write("Python\n")
    file.write("File Handling\n")

print("sample.txt created")

# Append new text

with open("sample.txt", "a") as file:
    file.write("This line was appended.\n")

print("Text appended.")