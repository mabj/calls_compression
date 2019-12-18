#!/usr/bin/python3
import sys
from common import *

def main(argc=0, argv=[]):
    generic_call(1, lineno())
    for i in range(3):
        generic_call(2, lineno())
    generic_call(3, lineno())

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
