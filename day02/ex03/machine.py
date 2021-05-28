#!/usr/bin/python3

import random
from beverages import *

class CoffeeMachine():
    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")
    
    class EmptyCup(HotBeverage):
        def __init__(self):
            self.name = "empty cup"
            self.price = 0.90
        def description(self):
            return "An empty cup?! Gimme my money back!"

    def __init__(self):
        self.serve_count = 0

    def repare(self):
        self.serve_count = 0

    def serve(self, menu: HotBeverage):
        if self.serve_count == 10:
            raise CoffeeMachine.BrokenMachineException()
        self.serve_count += 1
        if random.randint(0, 10) > 8:
            return self.EmptyCup()
        return menu()

def main():
    machine = CoffeeMachine()
    for _ in range(22):
        try:
            print(machine.serve(random.choice([Chocolate, Cappuccino, Tea, Coffee])))
            print("\n=========================  [" + str(machine.serve_count) + "] sold\n")
        except CoffeeMachine.BrokenMachineException as e:
            print("\n\n       [machine broken!! It need repare!!]       \n\n")
            print(e)
            machine.repare()

if __name__ == '__main__':
    main()
