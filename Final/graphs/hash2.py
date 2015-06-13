#!/usr/bin/env python

import sys
import hashlib

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(blocksize), ""):
            hash.update(block)
    return hash.hexdigest()

if __name__ == "__main__":

    filename = "out.txt"
    print filename + " " + md5sum(filename, False)
