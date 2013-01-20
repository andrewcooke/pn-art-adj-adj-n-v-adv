#!/usr/bin/env python

import fileinput
import sys

from pnartadjadjnvadv.pre.bktree import BKtree

sys.setrecursionlimit(10000)


if __name__ == '__main__':
    
    for word in BKtree(map(lambda x: x.strip(), fileinput.input()), threshold=1).nodes.keys():
        print(word)
