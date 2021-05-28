#!/usr/bin/python3

class HotBeverage:
    def __init__(self) -> None:
        self.price = 0.30
        self.name = "hot beverage"
    def description(self) -> str:
        return "Just some hot water in a cup."
    def __str__(self):
        return ("name : " + self.name + '\n' + "price : " + "{0:0.2f}".format(self.price) + '\n' + "description : " + self.description())

class Coffee(HotBeverage):
    def __init__(self) -> None:
        self.price = 0.40
        self.name = "coffee"
    def description(self) -> str:
        return "A coffee, to stay awake."

class Tea(HotBeverage):
    def __init__(self) -> None:
        self.price = 0.30
        self.name = "tea"

class chocolate(HotBeverage):
    def __init__(self) -> None:
        self.price = 0.50
        self.name = "chocolate"
    def description(self) -> str:
        return "Chocolate, sweet chocolate..."

class Cappuccino(HotBeverage):
    def __init__(self) -> None:
        self.price = 0.45
        self.name = "cappuccino"
    def description(self) -> str:
        return "Un po’ di Italia nella sua tazza!"

def main():
    a = Coffee()
    print(a)
    print("\n\n\n")
    a = Tea()
    print(a)
    print("\n\n\n")
    a = chocolate()
    print(a)
    print("\n\n\n")
    a = Cappuccino()
    print(a)

if __name__ == '__main__':
    main()
