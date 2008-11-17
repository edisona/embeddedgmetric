#!/usr/bin/env python

import metric
from os import uname
ostype = uname()[0]
if ostype == 'Linux':
    from metrics_linux import *
elif ostype == 'Darwin':
    from metrics_darwin import *
else:
    print "whoops"
    sys.exit(1)


from subprocess import Popen, PIPE
import sched
from time import time, sleep
import sys
import socket

from collections import defaultdict
from gmetric import gmetric_read
from socket import gethostname

class monitortree(object):
    def __init__(self):
        self.hosts = defaultdict(dict)
        self.hostname = gethostname()

    def addMetric(self, values, host=None):
        # HOST -> METRICS -> VALUES

        # add timestamp to figureout node expiration
        values['_now'] = time()

        # TBD: replace with defaultdict
        if host is None:
            host = self.hostname

        metrics = self.hosts[host]
        name = values['NAME']
        metrics[name] = values

    def xml(self):
        parts = []

        # TBD: look at Ganglia 3
        parts.append('<GANGLIA_XML VERSION="2.5.7" SOURCE="gmond">\n')
        for host,metrics in self.hosts.iteritems():
            parts.append('<HOST name="%s">\n' % host)
            zap = []
            for name, values in metrics.iteritems():

                # figure out if this node "expired"
                expires = 0
                if '_now' in values and 'TMAX' in values:
                    now = time()
                    tmax = float(values['TMAX'])
                    if tmax > 0:
                        expires = float(values['_now']) + float(values['TMAX'])
                if expires and expires < now:
                    zap.append(values['NAME'])
                    continue
                
                # print the node
                parts.append('<METRIC NAME="' + values['NAME'] + '"')
                for k,v in values.iteritems():
                    if k != '_now' and k != 'NAME':
                        parts.append(' ' + k + '="' + str(v) + '"')
                parts.append('/>\n')

            # delete the expired nodes
            for name in zap:
                del metrics[name]

            parts.append('\n</HOST>\n')
        parts.append('</GANGLIA_XML>\n')
        return ''.join(parts)


# THREE THREADS
#  * writers
#  * receiver
#  * monitor
#
#

import threading
class Monitor(threading.Thread):
    def __init__(self, tree):
        threading.Thread.__init__(self)
        self.tree = tree
        
    def run(self):
        # MACHINE    
        s = sched.scheduler(time, sleep)
        
        for m in [metric_cpu(), metric_iostat(), metric_swap(), metric_disk(),
                  metric_proc_total(), metric_sys_clock(), metric_net()]:
            m.register(s, self.tree)
        
        s.run()

class Reader(threading.Thread):
    """
    Accepts UDP XDR gmetric packets
    """
    def __init__(self, tree):
        threading.Thread.__init__(self)
        self.tree = tree

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serversocket.bind(('', 4001))
        #serversocket.listen(5)

        tree = self.tree
        while 1:
            #accept connections from outside
            data, address = serversocket.recvfrom(512)
            tree.addMetric(gmetric_read(data))

class Writer(threading.Thread):
    """
    Writes out metrics tree as XML
    """
    def __init__(self, tree):
        threading.Thread.__init__(self)
        self.tree = tree

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('', 4000))
        serversocket.listen(5)
        while 1:
            clientsocket, address = serversocket.accept()
            clientsocket.send(self.tree.xml())
            clientsocket.close()

if __name__ == '__main__':
    
    tree =  monitortree()
    
    w = Writer(tree)
    w.start()

    r = Reader(tree)
    r.start()

    m = Monitor(tree)
    m.start()

