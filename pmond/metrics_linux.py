"""
Core metrics for Linux

Tested on  Linux Kernel 2.6.27.7.11, Ubuntu 8.10
"""

from subprocess import Popen, PIPE
from time import time

from metric import metric

class metric_proc_total(metric):
    def interval(self):
        return 80

    def gather(self, tree):
        p = Popen(['ps', '-ax'],  stdout=PIPE)    
        lines = p.stdout.read().split('\n')
        self.addMetric({'NAME':'proc_total', 'VAL':len(lines) -1,
                        'TYPE':'uint32', 'UNITS':'', 'TMAX':950,
                        'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})    
        
class metric_sys_clock(metric):
    def interval(self):
        return 1200

    def gather(self, tree):
        self.addMetric({'NAME':'sys_clock', 'VAL':int(time()),
                        'TYPE':'timestamp', 'UNITS':'s', 'TMAX':1200,
                        'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})    

class metric_swap(metric):
    def interval(self):
        return 40

    def gather(self, tree):
        f = open('/proc/meminfo', 'rb')
        lines = f.read().split('\n')
        f.close()

        swap_total = 0
        swap_free = 0
        for line in lines:
            if line.startswith('SwapTotal:'):
                swap_total = int(line[10:-3])
            elif line.startswith('SwapFree:'):
                swap_free = int(line[10:-3])
            
        self.addMetric({'NAME':'swap_total', 'VAL':swap_total,
                        'TYPE':'uint32', 'UNITS':'KB', 'TMAX':1200,
                        'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})

        self.addMetric({'NAME':'swap_free', 'VAL':swap_free,
                        'TYPE':'uint32', 'UNITS':'KB', 'TMAX':180,
                        'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})

class metric_cpu(metric):
    def interval(self):
        return 20

    def gather(self, tree):
        sysctls = [ 'sysctl',
                    'kern.ostype',
                    'kern.osrelease',
                    ]
        p = Popen(sysctls, stdout=PIPE)
        lines = p.stdout.read().split('\n')
        os_name = lines[0].split(' ')[1]
        os_release = lines[1].split(' ')[2]
        self.addMetric({'NAME':'os_name', 'VAL':os_name,
                        'TYPE':'string', 'UNITS':'', 'TMAX':1200,
                        'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})

        self.addMetric({'NAME':'os_release', 'VAL':os_release,
                        'TYPE':'string', 'UNITS':'', 'TMAX':1200,
                        'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})


        f = open('/proc/uptime', 'rb')
        lines = f.read()
        f.close()
        boottime = int(time() - float(lines.split(' ')[0]))
        self.addMetric({'NAME':'boottime', 'VAL': boottime,
                        'TYPE':'uint32', 'UNITS':'KB', 'TMAX':1200,
                        'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})

        f = open('/proc/cpuinfo', 'rb')
        lines = f.read().split('\n')
        f.close()

        cpu_num = 0
        cpu_speed = 0
        for line in lines:
            k,v = line.split(':',2)
            k = k.strip()
            if k.startswith('processor'):
                cpu_num += 1
            elif k.startswith('cpu MHz'):
                cpu_speed = int(v.strip())

         self.addMetric({'NAME':'cpu_num', 'VAL': cpu_num
                         'TYPE':'uint32', 'UNITS':'', 'TMAX':1200,
                         'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})        
         self.addMetric({'NAME':'cpu_speed', 'VAL': cpu_speed,
                         'TYPE':'uint32', 'UNITS':'MHz', 'TMAX':1200,
                         'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})

         # machine type.  gmond hardwires stuff at compile time with
         # a few types.  This is more dynamic

         p = Popen(['uname', '-m'], stdout=PIPE)
         line = p.stdout.read()
         machine_type = line.strip()
         self.addMetric({'NAME':'machine_type', 'VAL':machine_time,
                         'TYPE':'string', 'UNITS':'', 'TMAX':1200,
                         'DMAX':0, 'SLOPE':'zero', 'SOURCE':'gmond'})
         
class metric_net(metric):
    last_time = time()
    last_bytes_out = -1
    last_bytes_in = -1

    def interval(self):
        return 40

    def gather(self, tree):
        now = time()
        interval = self.last_time - now

        f = open('/proc/net/dev', 'rb')
        lines = f.read().split('\n')
        f.close()

        bytes_out = 0
        packets_out = 0
        bytes_in = 0
        bytes_out = 0

        for line in lines[2:]:
            interface = line[0:7]
            if interace == 'lo':
                # skip loopback interface?
                continue

            fields = filter(lambda x: len(x), line[7:].split(' '))
            bytes_out   += int(fields[0])
            packets_out += int(fields[1])
            bytes_in    += int(fields[8])
            packets_n   += int(fields[9])
        
        # Ideally you'd just return total_out and total_in
        # and let RRD figure out bytes/sec using a COUNTER
        # and call it a day

        # BUT, oddly  "official" gmond returns bytes per second 
        # which seems odd.  So sadly, we have do all this nonsense
        if self.last_bytes_out == -1:
            self.last_bytes_out   = bytes_out
            self.last_bytes_in    = bytes_in
            self.last_packets_out = packets_out
            self.last_packets_in  = packets_in
            return
        
        bytes_out_bps   = float(bytes_out   - self.last_bytes_out)   / interval
        bytes_in_bps    = float(bytes_in    - self.last_bytes_in)    / interval
        packets_out_bps = float(packets_out - self.last_packets_out) / interval
        packets_in_bps  = float(packets_in  - self.last_packets_in)  / interval

        self.last_time = time()
        self.last_bytes_out   = bytes_out
        self.last_bytes_in    = bytes_in
        self.last_packets_out = packets_out
        self.last_packets_in  = packets_in

        self.addMetric({'NAME':'bytes_in', 'VAL':bytes_in_bps,
                        'TYPE':'float', 'UNITS':'bytes/sec',
                        'TMAX':300, 'DMAX': 0, 'SLOPE':'both',
                        'SOURCE':'gmond'})
        self.addMetric({'NAME':'bytes_out', 'VAL':bytes_out_bps,
                        'TYPE':'float', 'UNITS':'bytes/sec',
                        'TMAX':300, 'DMAX': 0, 'SLOPE':'both',
                        'SOURCE':'gmond'})
        self.addMetric({'NAME':'packets_in', 'VAL':packets_in_bps,
                        'TYPE':'float', 'UNITS':'bytes/sec',
                        'TMAX':300, 'DMAX': 0, 'SLOPE':'both',
                        'SOURCE':'gmond'})
        self.addMetric({'NAME':'packets_out', 'VAL':packets_out_bps,
                        'TYPE':'float', 'UNITS':'bytes/sec',
                        'TMAX':300, 'DMAX': 0, 'SLOPE':'both',
                        'SOURCE':'gmond'})

class metric_mem(metric):
    """
    boh
    """

    def interval(self):
        return 60

    def gather(self, tree):
        f = open('/proc/meminfo', 'rb')
        lines = f.read().split('\n')
        f.close()
        swap_total = -1
        swap_free = -1
        for line in lines:
            if line.startswith('SwapTotal:'):
                swap_total = int(line.split()[1])
            elif line.startswith('SwapFree:'):
                swap_free = int(line.split()[1])

        if swap_total != -1:
            self.addMetric({'NAME':'swap_total','VAL' : swap_total,
                            'TYPE':'uint32', 'UNITS':'KB', 'TMAX':180,
                            'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})

        if swap_free != -1:
            self.addMetric({'NAME':'swap_free', 'VAL' : swap_free
                            'TYPE':'uint32', 'UNITS':'KB', 'TMAX':180,
                            'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})

        
class metric_disk(metric):
    def interval(self):
        return 40

    def gather(self, tree):
        p = Popen(['df', '-m', '/'], stdout=PIPE)
        lines = p.stdout.read().split('\n')

        fields = lines.split()
        disk_total = float(values[1]) /  1048576.0
        disk_free = float(values[3]) /  1048576.0
            
        self.addMetric({'NAME':'disk_total', 
                        'VAL' : disk_total,
                        'TYPE':'double', 'UNITS':'GB', 'TMAX':1200,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})

        self.addMetric({'NAME':'disk_free', 
                        'VAL' : disk_free,
                        'TYPE':'double', 'UNITS':'GB', 'TMAX':1200,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})


class metric_iostat(metric):
    last_time = -1
    cpus = []

    def interval(self):
        return 20

    def gather(self, tree):
        f = open('/proc/stat', 'rb')
        line = f.stdout.readline()
        c.close()

        fields = line.split()
        cpus = [int(fields[1]), int(fields[2]), int(fields[3]),int(fields[4])]

        if self.last_time = -1:
            self.last_time = time()
            self.cpus = cpus
            return

        # convert to zip
        cpu_diff = [float(cpus[i] - self.cpus[i]) for i in range(4)]
        cpu_sum = float(sum(cpu_diff))
        cpu_percent = [ 100.0 * cpus[i]/ cpu_sum for in range(4) ]

        self.addMetric({'NAME':'cpu_user', 'VAL': cpu_percent[0],
                        'TYPE':'float', 'UNITS':'%', 'TMAX':90,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})
        self.addMetric({'NAME':'cpu_nice', 'VAL': cpu_percent[1],
                        'TYPE':'float', 'UNITS':'%', 'TMAX':90,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})
        self.addMetric({'NAME':'cpu_system', 'VAL':cpu_percent[2],
                        'TYPE':'float', 'UNITS':'%', 'TMAX':90,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})
        self.addMetric({'NAME':'cpu_idle', 'VAL':cpu_percent[3],
                        'TYPE':'float', 'UNITS':'%', 'TMAX':90,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})

        f = open('/proc/loadavg', 'rb')
        line = f.read().split(' ')
        f.close()

        load_one = float(line[0])
        load_five = float(line[1])
        load_fifteen = float(line[2])

        self.addMetric({'NAME':'load_one', 'VAL':load_one,
                        'TYPE':'float', 'UNITS':'%', 'TMAX':90,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})
        self.addMetric({'NAME':'load_five', 'VAL':load_five,
                        'TYPE':'float', 'UNITS':'%', 'TMAX':90,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})
        self.addMetric({'NAME':'load_fifteen', 'VAL':load_fifteen,
                        'TYPE':'float', 'UNITS':'%', 'TMAX':90,
                        'DMAX':0, 'SLOPE':'both', 'SOURCE':'gmond'})


