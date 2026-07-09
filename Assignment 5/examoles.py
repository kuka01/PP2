import re

text = "Python 123 is AWESOME."

print("search")
print(re.search("Python", text))

print()

print("findall")
print(re.findall(r"\d", text))

print()

print("split")
print(re.split(" ", text))

print()

print("sub")
print(re.sub("Python", "Java", text))

print()

print("match")
print(re.match("Python", text))

print()

print("Digits")
print(re.findall(r"\d", text))

print()

print("Words")
print(re.findall(r"\w+", text))

print()

print("Spaces")
print(re.findall(r"\s", text))

print()

print("Uppercase")
print(re.findall(r"[A-Z]", text))

print()

print("Lowercase")
print(re.findall(r"[a-z]", text))

print()

print("Starts with P?")
print(re.match(r"^P", text))

print()

print("Ends with dot?")
print(re.search(r"\.$", text))