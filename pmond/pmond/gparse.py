#!/usr/bin/env python
from lxml import etree
import urllib2
import os.path
import os
import time
# http://packages.ubuntu.com/intrepid/python-rrd
import rrdtool

class gparse:
    def __init__(self):
        self.hosts = {}

    def parse_string(self, s):
        hosts = self.hosts
        root = etree.XML(s)
        for host in root.iter('HOST'):
            name = host.get('name')
            hosts[name] = {}
            metrics = hosts[name]
            for m in host.iter('METRIC'):
                  metrics[m.get('NAME')] = m.attrib
        return True

    def parse_url(self, s):
        #
        try:
            f = urllib2.urlopen(s)
            data = f.read()
            f.close()
            return self.parse_string(data)
        except:
            return False
        #print repr(self.hosts)
        #print self.hosts['nickg-macbook.local']['cpu_speed']['VAL']

    def parse_file(self, s):
        f = open(s)
        data = f.read()
        f.close()
        return parse_string(data)

    def make_graph_load(self, dir, host, duration, width):
        """ Specialized fform for Load Graphs"""
        # this oculd be imporved by just reusing the 1-m load
        # instead of using 1,5,15 metrics, but whatever

        f = host + '-load-' + duration + '-' + str(width) + '.png' 
        path = os.path.join(dir, host)

        imgfile = os.path.join(path, f)
        # if less than X seconds old, just return imgfile
        
        load1_rrdfile = os.path.join(path, "load_one.rrd")
        load5_rrdfile = os.path.join(path, "load_five.rrd")
        load15_rrdfile = os.path.join(path, "load_fifteen.rrd")

        rrdtool.graph(imgfile,
                      '--end', 'now',
                      '--start', 'end-' + duration,
                      '--width', width,
                      '--imgformat', 'PNG',
                      '--lower-limit', '0',
                      '--title', 'Load',
                      'DEF:l1=' + load1_rrdfile + ':load_one:AVERAGE',
                      'DEF:l5=' + load5_rrdfile + ':load_five:AVERAGE',
                      'DEF:l15=' + load15_rrdfile + ':load_fifteen:AVERAGE',
                      'LINE1:l1#0000FF:"load 1"',
                      'LINE1:l5#00FF00:"load 5"',
                      'LINE1:l15#FF0000:"load 15"'
                      )

        return imgfile

    def make_graph_cpu(self, dir, host, duration, width):
        """ Specialized form for CPU graphs """
        
        f = host + '-cpu-' + duration + '-' + str(width) + '.png' 
        path = os.path.join(dir, host)

        imgfile = os.path.join(path, f)

        sys_rrdfile = os.path.join(path, "cpu_system.rrd")
        user_rrdfile = os.path.join(path, "cpu_user.rrd")
        nice_rrdfile = os.path.join(path, "cpu_nice.rrd")

        rrdtool.graph(imgfile,
                      '--end', 'now',
                      '--start', 'end-' + duration,
                      '--width', width,
                      '--imgformat', 'PNG',
                      '--lower-limit', '0',
                      '--upper-limit', '100',
                      '--title', 'CPU Usage',
                      'DEF:sys=' + sys_rrdfile + ':cpu_system:AVERAGE',
                      'DEF:user=' + user_rrdfile + ':cpu_user:AVERAGE',
                      'DEF:nice=' + nice_rrdfile + ':cpu_nice:AVERAGE',
                      'LINE1:sys#0000FF:"cpu system"',
                      'AREA:user#00FF00:"cpu user":STACK',
                      'AREA:nice#FF0000:"cpu nice":STACK'
                      )
        return imgfile

    def make_graph_network(self, dir, host, duration, width):
        """ Specialized form for CPU graphs """
        
        f = host + '-network-' + duration + '-' + str(width) + '.png' 
        path = os.path.join(dir, host)
        imgfile = os.path.join(path, f)

        bytesin_rrdfile = os.path.join(path, "bytes_in.rrd")
        bytesout_rrdfile = os.path.join(path, "bytes_out.rrd")

        rrdtool.graph(imgfile,
                      '--end', 'now',
                      '--start', 'end-' + duration,
                      '--width', width,
                      '--imgformat', 'PNG',
                      '--lower-limit', '0',
                      '--title', 'Network Bytes',
                      'DEF:bi=' + bytesin_rrdfile + ':bytes_in:AVERAGE',
                      'DEF:bo=' + bytesout_rrdfile + ':bytes_out:AVERAGE',
                      'LINE1:bi#0000FF:bytes in',
                      'LINE1:bo#FF0000:bytes out'
                      )
        return imgfile

    def make_graph_memory(self, dir, host, duration, width):
        """ Specialized form for CPU graphs """

        f = host + '-memory-' + duration + '-' + str(width) + '.png' 
        path = os.path.join(dir, host)
        imgfile = os.path.join(path, f)
        
        path = os.path.join(dir, host)
        mem_rrdfile = os.path.join(path, "mem_used_percent.rrd")
        swap_rrdfile = os.path.join(path, "swap_used_percent.rrd")
        disk_rrdfile = os.path.join(path, "disk_used_percent.rrd")

        rrdtool.graph(imgfile,
                      '--end', 'now',
                      '--start', 'end-' + duration,
                      '--width', '400',
                      '--imgformat', 'PNG',
                      '--lower-limit', '0',
                      '--upper-limit', '100',

                      '--title', '% of Memory,Swap,Disk Used',
                      'DEF:bi=' + mem_rrdfile + ':mem_used_percent:AVERAGE',
                      'DEF:bo=' + swap_rrdfile + ':swap_used_percent:AVERAGE',
                      'DEF:disk=' + disk_rrdfile + ':disk_used_percent:AVERAGE',
                      'LINE1:bi#0000FF:memory used',
                      'LINE1:bo#FF0000:swap used',
                      'LINE1:disk#FF0000:disk used'
                      )
        return imgfile

    def make_graph(self, dir, host, metric, duration, width='400'):
        #--end now --start end-120000s --width 400
        
        if metric == 'cpu':
            return self.make_graph_cpu(dir,host,duration,width)
        if metric == 'network':
            return self.make_graph_network(dir,host,duration,width)
        if metric == 'memory':
            return self.make_graph_memory(dir,host,duration,width)
        if metric == 'load':
            return self.make_graph_load(dir,host,duration,width)

        f = host + '-' + metric + '-' + duraton + '-' + str(width) + '.png' 
        path = os.path.join(dir, host)
        imgfile = os.path.join(path, f)

        rrdfile = os.path.join(path, metric + ".rrd")

        rrdtool.graph(imgfile,
                      '--end', 'now',
                      '--start', 'end-' + duration,
                      '--width', '400',
                      '--imgformat', 'PNG',
                      '--title', metric,
                      'DEF:ds0a=' + rrdfile + ':' + metric + ':AVERAGE',
                      'LINE1:ds0a#0000FF:"default resolution\l"'
                      )
        return imgfile

    def make_rrds(self, dir):
        for host, metrics in self.hosts.iteritems():
            path = os.path.join(dir, host)
            if not os.path.isdir(path):
                os.mkdir(path)

            # memory & swap
            # CPU
            # network in/out
            # load
            did_mem = False
            did_swap = False
            crawlers = {}
            
            for mname, attrs in metrics.iteritems():
                if mname.startswith('mem_') or mname.startswith('swap_') or mname.startswith('pkts_') or mname.startswith('disk_'):
                    continue
                rrdfile = os.path.join(path, mname + ".rrd")
                self.rrd_update(rrdfile,  attrs['NAME'], attrs['VAL'], attrs['SLOPE'])
                if mname.startswith('c') and mname.endswith('_name'):
                    cid,cname = mname.split('_')
                    crawlers[cid] = cname

            name = 'num_crawlers'
            rrdfile = os.path.join(path, name + '.rrd')
            self.rrd_update(rrdfile, name, len(crawlers), 'both')

            # ignore these, and just use how much is used
            mem_total = float(metrics['mem_total']['VAL'])
            mem_free = float(metrics['mem_free']['VAL'])
            name = 'mem_used_percent'
            rrdfile = os.path.join(path, name + ".rrd")
            self.rrd_update(rrdfile, name, 100.0 * (1.0 - mem_free / mem_total), 'both')

            swap_total = float(metrics['swap_total']['VAL'])
            swap_free  = float(metrics['swap_free']['VAL'])
            name = 'swap_used_percent'
            rrdfile = os.path.join(path, name + ".rrd")
            self.rrd_update(rrdfile, name, 100.0 * (1.0 - swap_free / swap_total), 'both')

            disk_total = float(metrics['disk_total']['VAL'])
            disk_free  = float(metrics['disk_free']['VAL'])
            name = 'disk_used_percent'
            rrdfile = os.path.join(path, name + ".rrd")
            self.rrd_update(rrdfile, name, 100.0 * (1.0 - disk_free / disk_total), 'both')

    def rrd_update(self, rrdfile, name, value, slope):
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

if __name__ == '__main__':

    g = gparse()
    #for i in xrange(100):
    #    if g.parse_url('http://localhost:4000/'):
    #        g.make_rrds('/tmp')
    #    time.sleep(1)

    g.make_graph('/tmp', 'ubuntu', 'cpu_idle', '60s')
    g.make_graph_cpu('/tmp', 'ubuntu', '60s')
    g.make_graph_load('/tmp', 'ubuntu', '300s')
    g.make_graph_network('/tmp', 'ubuntu', '300s')
    g.make_graph_memory('/tmp', 'ubuntu', '300s')


#
# CPU
#
#
