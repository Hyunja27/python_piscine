#!/usr/bin/python3

import sys

def capital_city(state_name):
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
    try:
        print(capital_cities[states[state_name]])
    except:
        print("Unknown state")

def main():
    if len(sys.argv) == 2:
        capital_city(sys.argv[1])

if __name__ == '__main__':
    main()