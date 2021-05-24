#!/usr/bin/python3

def main():
    line = open("numbers.txt", 'r').read().strip().split(',')
    for i in line:
        print(i)

if __name__ == '__main__':
    main()