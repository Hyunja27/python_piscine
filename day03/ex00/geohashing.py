#!/usr/bin/python3

import sys 
import antigravity

def main():
    if len(sys.argv)!=4:
        print("arg num is not right")
        return
    try :
        float(sys.argv[1])
        float(sys.argv[2])
    except:
        print("arg is cannot to be float")
        return
    antigravity.geohash(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3].encode())

if __name__=='__main__':
    main()
