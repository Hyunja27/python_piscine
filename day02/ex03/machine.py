#!/usr/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    machin.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: spark <spark@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/05/25 16:29:15 by spark             #+#    #+#              #
#    Updated: 2021/05/25 16:29:16 by spark            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
from beverages import *

class EmptyCup(HotBeverage):
    def __init__(self):
        self.name = "empty cup"
        self.price = 0.90

    def description(self):
        return "An empty cup?! Gimme my money back!"


class CoffeeMachine():
    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self.serve_count = 0
        self.cup = EmptyCup()
        self.tea = Tea()
        self.coffee = Coffee()
        self.cappuccino = Cappuccino()
        self.chocolate = Chocolate()

    def repare(self):
        self.serve_count = 0

    def serve(self, menu: HotBeverage):
        if self.serve_count == 10:
            raise CoffeeMachine.BrokenMachineException()
        self.serve_count += 1
        if random.randint(0, 10) > 8:
            return self.cup
        return menu()

def main():
    machine = CoffeeMachine()
    for _ in range(20):
        try:
            print(machine.serve(random.choice([Chocolate, Cappuccino, Tea, Coffee])))
            print("\n=========================  [" + str(machine.serve_count) + "] sold\n")
        except CoffeeMachine.BrokenMachineException as e:
            print("\n\n       [machine broken!! repare!!]       \n\n")
            print(e)
            machine.repare()

if __name__ == '__main__':
    main()
