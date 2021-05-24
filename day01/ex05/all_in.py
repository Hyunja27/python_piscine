#!usr/bin/python3

import sys

def get_val(dic: dict, target:str):
    for key, value in dic.items():
        if key.lower() == target.lower():
            return value
    return None

def get_key(dic: dict, target:str):
    for key, value in dic.items():
        if value.lower() == target.lower():
            return key
    return None

def all_in(val):
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    for target in val:
        target = target.strip()
        if target == "":
            continue

        a = get_val(states , target)
        b = get_key(capital_cities , target)
        if a:
            print(get_val(capital_cities , a) ,"is the capital of", get_key(states, a))
        elif b:
            print(get_val(capital_cities, b),"is the capital of", get_key(states , b))
        else:
            print(target, "is neither a capital city nor a state")

def main():
    if len(sys.argv) == 2:
        li = sys.argv[1].split(',')
        all_in(li)

if __name__=='__main__':
   main()
