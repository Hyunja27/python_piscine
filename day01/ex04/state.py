# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    state.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: spark <spark@student.42seoul.kr>           +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/05/25 09:07:49 by spark             #+#    #+#              #
#    Updated: 2021/05/25 09:07:50 by spark            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!usr/bin/python3

import sys

def state(capital):
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
    invert_state = {y: x for x, y in states.items()}
    invert_capitals = {y: x for x, y in capital_cities.items()}
    try:
        print(invert_state[invert_capitals[capital]])
    except:
        print("Unknown capital city")


def main():
    if len(sys.argv) == 2:
        state(sys.argv[1])

if __name__ == '__main__':
    main()