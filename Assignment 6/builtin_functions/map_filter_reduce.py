from functools import reduce

numbers = [1,2,3,4,5]

print("map()")

square = list(map(lambda x: x*x, numbers))

print(square)

print()

print("filter()")

even = list(filter(lambda x: x % 2 == 0, numbers))

print(even)

print()

print("reduce()")

total = reduce(lambda x, y: x + y, numbers)

print(total)