import math
import random

print("Built-in Math Functions")

print("Min:", min(4, 7, 2, 9))
print("Max:", max(4, 7, 2, 9))
print("Abs:", abs(-20))
print("Round:", round(4.76))
print("Power:", pow(2, 5))

print("\nMath Module")

print("Square Root:", math.sqrt(64))
print("Ceil:", math.ceil(4.3))
print("Floor:", math.floor(4.8))
print("Sin(90°):", math.sin(math.radians(90)))
print("Cos(0°):", math.cos(math.radians(0)))
print("Pi:", math.pi)
print("e:", math.e)

print("\nRandom Module")

print("Random Integer:", random.randint(1, 100))

names = ["John", "Alice", "Bob", "Mike"]

print("Random Choice:", random.choice(names))

random.shuffle(names)

print("Shuffled List:", names)