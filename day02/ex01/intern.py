#!/bin/python3

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

def main():
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