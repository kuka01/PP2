names = ["John","Alice","Mike"]

print("enumerate()")

for index, value in enumerate(names):
    print(index, value)

print()

subjects = ["Math","Physics","Python"]

print("zip()")

for name, subject in zip(names, subjects):
    print(name, subject)

print()

print("Type Conversion")

number = "25"

print(int(number))

price = 10

print(float(price))

print(str(price))