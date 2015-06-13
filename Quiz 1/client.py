#!/usr/bin/env python
# client.py

import config as cfg
import sys
import socket

def main():
    try:
        e = "go"
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        client.connect((host, cfg.PORT))
        client.send(e)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    except Exception as msg:
        print msg

#########################################################

if __name__ == "__main__":
    main()
