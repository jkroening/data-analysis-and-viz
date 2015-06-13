#!/usr/bin/env python
# server.py

import socket
import select
import config as cfg
import Queue
from threading import Thread
from time import sleep
from random import gauss
from random import randint
import sys

class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()

    def add(self, data):
        self.q.put(data)

    def stop(self):
        self.running = False

    def run(self):
        q = self.q
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                process(value)
            except Queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()
        #
        if not q.empty():
            print "Elements left in the queue:"
            while not q.empty():
                print q.get()

t = ProcessThread()
t.start()

def process(value):
    """
    Implement this. Do something useful with the received data.
    """
    print value
    # sleep(randint(1,9))    # emulating processing time

def main():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = cfg.PORT                # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port
    print "Listening on port {p}...".format(p=port)

    s.listen(5)                 # Now wait for client connection.
    while True:
        try:
            client, addr = s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                # generate random Los Angeles weather data
                temp = round(gauss(65.4, 6)) #Gaussian distribution (mean, std.dev) of Los Angeles yearly mean temperatures
                degree_symbol = u'\xb0F'.encode("UTF-8")
                temperature = "%d%s" % (temp, degree_symbol)
                hum = round(gauss(65, 10)) #Gaussian distribution (mean, std.dev) of Los Angeles yearly mean humidity
                humidity = "%d%% humidity" % hum
                cc = round(gauss(15, 10)) #Gaussian distribution (mean, std.dev) of Los Angeles yearly median cloud cover
                cloudcover = "%d%% clear skies (%d%% cloud cover)" % (100-cc, cc)
                data = {'temperature' : temperature, 'humidity' : humidity, 'cloudcover' : cloudcover}
                # data = client.recv(4096)
                #print data
                t.add("Current weather in Downtown Los Angeles: %s, %s, and %s" % (data['temperature'], data['humidity'], data['cloudcover']))
        except KeyboardInterrupt:
            print
            print "Stop."
            break
        except socket.error, msg:
            print "Socket error! %s" % msg
            break
    #
    cleanup()

def cleanup():
    t.stop()
    t.join()

#########################################################

if __name__ == "__main__":
    main()
