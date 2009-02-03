#!/usr/bin/env python

import urllib2
import os.path
import os
import time

import rrdtool
from lxml import etree

import gparse

def rrd_update(rrdfile, name, value, slope):

    # fix annoying unicode issues
    rrdfile = str(rrdfile)
    
    dstype = 'GAUGE'
    if slope == 'zero':
        dstype = 'ABSOLUTE'
        # for now don't care about invariants
        return
    elif slope == 'both':
        dstype = 'GAUGE'
    elif slope == 'positive':
        dstype = 'COUNTER'
        
    token = 'DS:' + name + ':' + dstype + ':20:U:U'
    if not os.path.exists(rrdfile):
        print "Creating ", rrdfile
        # 1440 is minutes per day
        # 300 minutes = 5 hours
        # 30 hours = 1800 minutes
        rrdtool.create(rrdfile, '--step=10', token,
                       # 1 point at 10s, 1800 of them 300m, 5 hours
                       'RRA:AVERAGE:0.5:1:1800',
                       # 6 points @ 10s = 60s = 1m, 30 hours
                       'RRA:AVERAGE:0.5:6:1800'
                       )
        # no else
    rrdtool.update(rrdfile, 'N:' + str(value))

def make_standard_rrds(hosts, dir):
    """
    walks the host mappings and makes
    specialized graphs for various metrics
    """
    for host, metrics in hosts.iteritems():
        path = os.path.join(dir, host)
        if not os.path.isdir(path):
            os.mkdir(path)

        for mname, val in metrics.iteritems():
            # stuff we don't care about
            if mname in ('boottime', 'gexec', 'machine_type', 'os_name',
                         'os_release'):
                continue
            if mname.startswith('multicpu_') or mname.startswith('pkts_'):
                continue

            # these are handled differently
            if mname.startswith('mem_') or \
                   mname.startswith('swap_') or \
                   mname.startswith('disk_'):
                continue
            
            rrdfile = os.path.join(path, mname + ".rrd")
            print "Adding %s = %s" % (mname, val)
            rrd_update(rrdfile, mname, val, 'both')

        if True:
            # gmond reports "total" and "used" (absolute numbers)
            #   making rrds of both isn't very useful
            # so I merge them and make a consolidated version
            # of "% of total used" which is normally more interesting
            
            mem_total = float(metrics['mem_total'])
            mem_free = float(metrics['mem_free'])
            name = 'mem_used_percent'
            rrdfile = os.path.join(path, name + ".rrd")
            rrd_update(rrdfile, name, 100.0 *
                       (1.0 - mem_free / mem_total), 'both')
            
            swap_total = float(metrics['swap_total'])
            swap_free  = float(metrics['swap_free'])
            name = 'swap_used_percent'
            rrdfile = os.path.join(path, name + ".rrd")
            rrd_update(rrdfile, name, 100.0 *
                       (1.0 - swap_free / swap_total), 'both')
            
            disk_total = float(metrics['disk_total'])
            disk_free  = float(metrics['disk_free'])
            name = 'disk_used_percent'
            rrdfile = os.path.join(path, name + ".rrd")
            rrd_update(rrdfile, name, 100.0 *
                       (1.0 - disk_free / disk_total), 'both')
        
if __name__ == '__main__':

    while True:
        xml = gparse.read('localhost', 8649)
        hosts = gparse.parse(xml)
        make_standard_rrds(hosts, '/tmp')
        time.sleep(10)

    if False:
        g.make_graph('/tmp', 'ubuntu', 'cpu_idle', '60s')
        g.make_graph_cpu('/tmp', 'ubuntu', '60s')
        g.make_graph_load('/tmp', 'ubuntu', '300s')
        g.make_graph_network('/tmp', 'ubuntu', '300s')
        g.make_graph_memory('/tmp', 'ubuntu', '300s')

