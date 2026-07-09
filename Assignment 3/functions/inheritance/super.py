class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    def speak(self):
        super().speak()
        print("Dog")