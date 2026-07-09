import json

# -------------------------------
# Python to JSON
# -------------------------------

student = {
    "name": "John",
    "age": 20,
    "city": "Almaty",
    "marks": [90, 85, 100]
}

print("Python Dictionary")

print(student)

print("\nConvert Python to JSON")

json_string = json.dumps(student, indent=4)

print(json_string)

# -------------------------------
# Write JSON File
# -------------------------------

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)

print("\nstudent.json created")

# -------------------------------
# Read JSON File
# -------------------------------

with open("student.json", "r") as file:
    data = json.load(file)

print("\nRead student.json")

print(data)

# -------------------------------
# JSON String -> Python
# -------------------------------

text = '{"country":"Kazakhstan","capital":"Astana"}'

country = json.loads(text)

print("\nJSON String to Python")

print(country)

# -------------------------------
# Read sample-data.json
# -------------------------------

try:
    with open("sample-data.json", "r") as file:
        sample = json.load(file)

    print("\nsample-data.json")

    print(sample)

except FileNotFoundError:
    print("\nsample-data.json not found")