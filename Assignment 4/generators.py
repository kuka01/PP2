# -------------------------------
# Iterators
# -------------------------------

fruits = ["apple", "banana", "orange"]

my_iterator = iter(fruits)

print("Iterator using next():")
print(next(my_iterator))
print(next(my_iterator))
print(next(my_iterator))

print("\nLoop through iterator:")

for fruit in fruits:
    print(fruit)

# -------------------------------
# Create custom iterator
# -------------------------------

class Numbers:
    def __iter__(self):
        self.num = 1
        return self

    def __next__(self):
        if self.num <= 5:
            value = self.num
            self.num += 1
            return value
        raise StopIteration

print("\nCustom Iterator:")

numbers = Numbers()

for x in numbers:
    print(x)

# -------------------------------
# Generator
# -------------------------------

def countdown(n):
    while n > 0:
        yield n
        n -= 1

print("\nGenerator Function:")

for number in countdown(5):
    print(number)

# -------------------------------
# Generator Expression
# -------------------------------

print("\nGenerator Expression:")

squares = (x ** 2 for x in range(1, 6))

for square in squares:
    print(square)