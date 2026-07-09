class Fly:
    def fly(self):
        print("I can fly")

class Swim:
    def swim(self):
        print("I can swim")

class Duck(Fly, Swim):
    pass

duck = Duck()

duck.fly()
duck.swim()