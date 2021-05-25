#!/usr/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    beverages.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: spark <spark@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/05/25 14:26:48 by spark             #+#    #+#              #
#    Updated: 2021/05/25 14:44:56 by spark            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


class HotBeverage:
    def __init__(self) -> None:
        self.price = str(0.30)
        self.name = "hot beverage"

    def description(self) -> str:
        return "Just some hot water in a cup."

    def __str__(self):
        return ("name : " + self.name + '\n' + "price : " + self.price + '0' + '\n' + "description : " + self.description())


class Coffee(HotBeverage):
    def __init__(self) -> None:
        self.price = str(0.40)
        self.name = "coffee"

    def description(self) -> str:
        return "Just some hot water in a cup."


def main():
    a = Coffee()
    print(a)


if __name__ == '__main__':
    main()
