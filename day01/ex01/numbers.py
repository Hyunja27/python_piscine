# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    numbers.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: spark <spark@student.42seoul.kr>           +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/05/25 09:08:36 by spark             #+#    #+#              #
#    Updated: 2021/05/25 09:08:37 by spark            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/python3

def main():
    line = open("numbers.txt", 'r').read().strip().split(',')
    for i in line:
        print(i)

if __name__ == '__main__':
    main()