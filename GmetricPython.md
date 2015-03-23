# Gmetric Python #

Using the GmetricProtocol it's a snap to write a gmond/gmetric client, Especially with python since it includes the XDR formatting natively.  The code provides a module and a command-line interface.

I'm not a python super-expert so any hints to make it more pythonic would be welcome.

## Source and Install ##

The source code is  [gmetric.py](http://embeddedgmetric.googlecode.com/svn/trunk/python/gmetric.py).  You can directly download using that link or it's included in the full distribution in the `python` directory.   There is a `setup.py` script and unit test.

If you download the tarball, "make" will do all this for you.

## Command Line Usage ##

The gmetric module also has a command-line interface:

```
$ ./gmetric.py --help
Usage: gmetric.py [options]

Options:
  -h, --help           show this help message and exit
  --protocol=PROTOCOL  The gmetric internet protocol, either udp or multicast,
                       default udp
  --host=HOST          The gmond host to recieve the data
  --port=PORT          The gmond port to recieve the data
  --name=NAME          The name of the metric
  --value=VALUE        The value of the metric
  --units=UNITS        The units for the value, e.g. 'kb/sec'
  --slope=SLOPE        The sign of the derivative of the value over time, one
                       of zero, positive, negative, both, default both
  --type=TYPE          The value data type, one of string, int8, uint8, int16,
                       uint16, int32, uint32, float, double
  --tmax=TMAX          The maximum time in seconds between gmetric calls,
                       default 60
  --dmax=DMAX          The lifetime in seconds of this metric, default=0,
                       meaning unlimited

$./gmetric.py --host=localhost --port=8649 --name=foo --value=bar --type=string --dmax=300
$
```