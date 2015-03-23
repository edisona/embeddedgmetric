Ganglia's gmetric is a handy command line tool to inject custom metrics into [gmond](http://ganglia.info/).  However it and `libganglia` are not designed for embedding into a C/C++ application.  Nor does it provide any scripting interface.

This project provide scripting modules that do not require `gmond.conf` or `gmetric` or any other dependencies (these are not wrappers around C code or call `gmetric`).  There is also a C/C++ library for embedding into applications.


| **Language** | **Wiki** | **Protocols** | **Dependencies** |
|:-------------|:---------|:--------------|:-----------------|
| C/C++    | GmetricClib | UDP only  | none -- self contained |
| Python   | GmetricPython | UDP, multicast | none -- _pure_ python, [one file](http://embeddedgmetric.googlecode.com/svn/trunk/python/gmetric.py) |
| Php      | GmetricPhp | UDP only       | none -- _pure_ php, [one file](http://embeddedgmetric.googlecode.com/svn/trunk/php/gmetric.php) |
| perl     | GmetricPerl | TBD | [one file](http://embeddedgmetric.googlecode.com/svn/trunk/perl/gmetric.pl) |
| Java     | GmetricJava | UDP, multicast |  none -- [one file](http://embeddedgmetric.googlecode.com/svn/trunk/gmetric3/java/gmetric3.java), [multicast project](http://embeddedgmetric.googlecode.com/svn/trunk/gmetric3/java/src/) |



## Benefits ##

The main benefit of embedded gmetric into your script or application is to avoid the overhead of
  * parsing `gmond.conf` (assuming it is available on your machine)
  * starting a new process
  * calling `gethostbyname` to resolve the socket

For the occasion metric, calling out to `gmetric` is not a problem.  However if you wanted to inject dozens (hundreds?) of statistics the overhead can slow you down.

## When not to use embeddedgmetric ##

You should continue to use regular `gmetric` if you have any type of special configuration that involve sending stats to multiple machines, sockets, multicast addresses.

Embedded gmetric primary is useful when you send stats to _one_ machine, especially when using UDP.

## News ##

### 17-Nov-2008 Version 1.3 relased ###
  * Fixed [Issue 5](https://code.google.com/p/embeddedgmetric/issues/detail?id=5) -- a horrible cut-n-paste error resulted in _two_ sockets being opened, not one.  Thanks to "benoit.louy" for reporting the issue.
  * Python gmetric.py is slightly improved as well.

### 20-Nov-2007 Version 1.2 released ###
  * Upgraded modp\_numtoa to get rounding bug fixes.  Only effects C/C++ versions.

### 17-May-2007 Version 1.1 released ###

  * Much improved makefiles and tests
  * Significant performance improvements by not using `sprintf`  (See [here](http://code.google.com/p/stringencoders/wiki/NumToA) for details).
  * Minor interface changes (some names changed so it doesn't collide with `ganglia.h`)
  * alpha prototypes for pure perl and php started
  * NO functional changes to the C or pure python versions



