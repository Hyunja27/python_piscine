#!usr/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    intern_practice.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: spark <spark@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/05/25 11:53:54 by spark             #+#    #+#              #
#    Updated: 2021/05/26 14:50:52 by spark            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Coffee:
    def __str__(self):
        return "This is the worst coffee you ever tasted."

class Intern:
    def __init__(self, Name=None) -> None:
        self.Name = Name
        if not Name:
            self.Name = "My name? I’m nobody, an intern, I have no name."

    def __str__(self) -> str:
        return self.Name

    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")
    
    def make_coffee(self) -> Coffee:
        return Coffee()

class Latte(Coffee):
    def __init__(self) -> None:
        self.milk = True
    def getMilk(self) -> bool:
        return self.milk
    def setMilk(self, bool):
        self.milk = bool

class Caramel_latte(Latte):
    def __init__(self) -> None:
        super().__init__()
        self.caramel = True
    def ingredient(self) -> bool:
        return super().getMilk()
    def milk_free_latte(self):
        if (super().getMilk() == True):
            print("아오 아직 우유가 있네!")
        super().setMilk(False)
        if (super().getMilk() == True):
            print("아오 아직 우유가 있네!")
        else:
            print("굿!!")
        

def main():
    a = Caramel_latte()
    b = Caramel_latte()

    if (b.ingredient() == True):
        print("b는 우유가 있습니당")
    else:
        print("b는 우유가 없습니당")

    b.milk_free_latte()
    
    if (b.ingredient() == True):
        print("b는 우유가 있습니당")
    else:
        print("b는 우유가 없습니당")
    a.milk_free_latte()
    
    
    if (a.ingredient() == True):
        print(a)
    just_intern = Intern()
    mark = Intern("Mark")
    print(just_intern)
    print(mark)
    print(mark.make_coffee())
    try:
        print(just_intern.work())
    except Exception as e:
        print(e)

if __name__=='__main__':
    main()