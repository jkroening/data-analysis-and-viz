#!/usr/bin/env python

import sys
import hashlib

CIN = "302300367"

def md5sum(filename, withCin, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(blocksize), ""):
            hash.update(block)
    if withCin:
      hash.update(CIN)
    return hash.hexdigest()

if __name__ == "__main__":

    min = 0
    max = 10000

    fp = open ("out.txt", "w")

    fp.write(CIN)
    fp.write("\n")
    for f in range(min,max):
      filename = '%04d' % f
      line = filename + " " + md5sum(filename, True)
      print line
      fp.write(line)
      fp.write("\n")
    fp.close()
