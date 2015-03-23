# Install #

## Red Hat Based Systems ##

You need 3 RPMs
  * libconfuse -- a config file parser -- probably doesn't have to be the most up-to-date version
  * libganglia -- the core libraries
  * gmond - the metrics collector/emitter/receiver.

There are few ways to get them:

### Manual RPM ###

```
# libconfuse
wget 'ftp://rpmfind.net/linux/EPEL/5/x86_64/libconfuse-2.5-4.el5.i386.rpm'
sudo rpm -ivh libconfuse-2.5-4.el5.i386.rpm

# libganglia
wget 'http://downloads.sourceforge.net/ganglia/libganglia-3_1_0-3.1.1-1.i386'
sudo rpm -ivh libganglia-3_1_0-3.1.1-1.i386.rpm

#
wget 'http://downloads.sourceforge.net/ganglia/ganglia-gmond-3.1.1-1.i386.rpm'
sudo rpm -ivh ganglia-gmond-3.1.1-1.i386.rpm
```

### YUM style ###

IIf you add  <a href='https://rpmrepo.org/RPMforge/Using'>RPM Forge</a> to your YUM repository list, then it should be as simple as

```
sudo yum install ganglia-gmond
```

# Starting and Stopping #

On RedHat systems, the daemon is installed, started, and added to `init.d` so it starts when the machine boots up.

For manual control, it should be:

```
/etc/init.d/gmond [start|stop|restart]
```


# Configuration #

Ok, here's the fun part.  The configuration file is located at `/etc/ganglia/gmond.conf`

Until you need it, I would comment out the `cluster`.  This just simplifies the outbound XML.

```
/*
cluster {
  name = "unspecified"
  owner = "unspecified"
  latlong = "unspecified"
  url = "unspecified"
}
*/
```

For right now, just use your current IP address for the `host` parameter, and set the following
```
udp_send_channel {
 host = 172.16.70.128  #OR WHATEVER
 port = 8649
}

udp_recv_channel {
  port = 8649
}

tcp_accept_channel {
  port = 8649
}
```

Now save the file and do
```
sudo /etc/init.d/gmond restart
```

Now,

```
# use localhost or whatever IP you used above
telnet localhost 8649
```

A whole-lotta XML should come back to you, perhaps ending like:

```
....
<METRIC NAME="swap_free" VAL="1543328.000" TYPE="float" UNITS="KB" TN="25" TMAX="180" DMAX="0" SLOPE="both">
<EXTRA_DATA>
<EXTRA_ELEMENT NAME="GROUP" VAL="memory"/>
<EXTRA_ELEMENT NAME="DESC" VAL="Amount of available swap memory"/>
<EXTRA_ELEMENT NAME="TITLE" VAL="Free Swap Space"/>
</EXTRA_DATA>
</METRIC>
</HOST>
</GANGLIA_XML>
```

Ta-da .. that's it.

# Next Steps #

  1. find a machine to use for your "metrics collection", and get it's IP address.
  1. insert it's IP address into the config file
  1. install just as above, gmond (and support libraries) on every box you wish to monitor
  1. maybe add a nagios check to make sure gmond is running

Once you have gmond running on all your boxes, the XML should have multiple `HOST` enteries.

You are now collecting metrics.

Next time... how to do graphing.