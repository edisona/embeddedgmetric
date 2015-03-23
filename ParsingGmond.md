# Introduction #

In this installment we are going to parse the output of gmond.

## Install ##

We are going to use [python](http://python.org) with  [lxml](http://codespeak.net/lxml/).   But this is so simple, it borders on use regular expressions.

For you YUM people, using the [RPMForge](https://rpmrepo.org/RPMforge/Using) repository, it should be as simple as

```
sudo yum install python-lxml
```

otherwise, you'll need [libxml2](http://xmlsoft.org/downloads.html) first, and manual install lxml.  It should be fairly straight forward.

## Getting the XML ##

Recall that just this:
```
telnet localhost 8649
```

gives you the XML.  gmond starts spitting back xml as soon as you _connect_.  No headers, no arguments.  If you send them, it will just ignore them.   All you have to do is  connect.    You can use `curl` and http to do this too

```
curl http://localhost:8649
```

### In Python ###

If you use http in python via [urllib2](http://docs.python.org/library/urllib2.html).  It gets mad that it's http headers were not read.  I'm not convinced python's networking stack is so great anyways, so we'll write a mini program that uses raw [sockets](http://docs.python.org/library/socket.html).

```
def read(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    data = ""
    while True:
        bytes = s.recv(4096)
        if len(bytes) == 0:
            break;
        data += bytes
    s.close()
    return data
```

This probably sucks, and doesn't handle error cases correctly, but seems to be ok for now.

## The XML ##

For some reason, gmond spits of a full DTD every request.  I do not know why.   Anyway if you are into that type thing, there it is.

Anyways, it's really simple:

```
<GANGLIA>
   <HOST NAME="172.16.70.128" ...  >
     <METRIC name="foo" value="bar" ... > ... </METRIC>
     <METRIC name="foo" value="bar" ... > ... </METRIC>
   </HOST>
   <HOST NAME="...">
     etc...
```


You'll see a lot of extra stuff.  most of it is self-explanitory.   Most of it I don't use, so the goal is strip this down.  Basically I want to do  `hosts[_host_][_metric_]` to get the value.

```
def parse(s):
    hosts = {}
    root = etree.XML(s)
    # newer versions could do:
    #for host in root.iter('HOST'):
    for host in root.findall('HOST'):
        name = host.get('NAME')
	hosts[name] = {}
        metrics = hosts[name]
        # new versions of lxml could do
        #for m in host.iter('METRIC'):
        for m in host.findall('METRIC'):
            metrics[m.get('NAME')] = m.attrib.get("VAL")
    return hosts
```

## Using it ##

Here's a simple driver program:

```
if __name__ == '__main__':
    s = read('localhost', 8649)
    hosts = parse(s)
    for h in hosts:
        print h
        keys = sorted(hosts[h])
        for k in keys:
            print "   %s = %s" % (k,hosts[h][k])
```

which on my VM prints:

```
$ ./gparse.py 
172.16.70.128
   boottime = 1233196822
   bytes_in = 569.77
   bytes_out = 444.83
   cpu_aidle = 97.9
   cpu_idle = 99.9
   cpu_nice = 0.0
   cpu_num = 2
   cpu_speed = 2194
   cpu_system = 0.1
   cpu_user = 0.0
   cpu_wio = 0.0
   disk_free = 2.126
   disk_total = 8.814
   gexec = OFF
   load_fifteen = 0.00
   load_five = 0.00
   load_one = 0.00
   machine_type = x86
   mem_buffers = 21988.000
   mem_cached = 251980.000
   mem_free = 402860.000
   mem_shared = 0.000
   mem_total = 783084.000
   multicpu_idle0 = 49.2
   multicpu_intr0 = 0.1
   multicpu_nice0 = 0.0
   multicpu_sintr0 = 0.0
   multicpu_system0 = 0.8
   multicpu_user0 = 0.0
   multicpu_wio0 = 0.0
   os_name = Linux
   os_release = 2.6.18-92.1.22.el5
   part_max_used = 76.5
   pkts_in = 6.37
   pkts_out = 3.45
   proc_run = 0
   proc_total = 97
   swap_free = 1572856.000
   swap_total = 1572856.000
```

### Next time... ###


This code is in svn [here](http://embeddedgmetric.googlecode.com/svn/trunk/pmond/pmond/gparse.py).  Go nuts!

Ok next time, we'll work on putting this data somewhere and graphing!