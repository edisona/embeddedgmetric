# The Gmetric Protocol #

The gmetric protocol as used by [ganglia](http://www.ganglia.info/) encodes raw data using XDR and strings.

## XDR Format ##

The XDR format is formally described in http://www.ietf.org/rfc/rfc4506.txt

Numeric types are stored as _big_ endian or 'network' order.  This is the same as what Java uses, and the native format of Sun and  PowerPC based machines.  This is different than what x86 machines use.

For integer types, any type that is 4 bytes, is converted to a full 32-bit integer type before being stored.  Specifically:
  * 32-bit integers: stored in big endian format.
  * 8-bit ('char'), 16-bit integers ('short'), stored as 32-bit integers.
  * enumerations: same as signed integers
  * boolean types, "0" is false, "1" is true, as signed integer

For floating point types:
  * 32-bit 'float' types -- standard IEEE format
  * 64-bit 'double' floating point types -- standard IEEE format

Strings are just a bit more complicated:
  * 32-bit unsigned integer n, the length of the data
  * n bytes of raw data
  * r bytes of padding, so (n+r) mod 4 == 0 (i.e. add enough zero bytes to n+r is a multiple of 4)

## Enumerations and Constants ##

```

enum ganglia_slope {
    GANGLIA_SLOPE_ZERO = 0,       ///< data is fixed, mostly unchanging
    GANGLIA_SLOPE_POSITIVE = 1,   ///< value is always increasing (counter)
    GANGLIA_SLOPE_NEGATIVE = 2,   ///< value is always decreasing
    GANGLIA_SLOPE_BOTH = 3,       ///< value can be anything
    GANGLIA_SLOPE_UNSPECIFIED = 4
};

static const char* typestrings[] = {
    "string",  // GANGLIA_VALUE_STRING
    "uint16",  // GANGLIA_VALUE_UNSIGNED_SHORT
    "int16",   // GANGLIA_VALUE_SHORT
    "uint32",  // GANGLIA_VALUE_UNSIGNED_INT
    "int32",   // GANGLIA_VALUE_INT
    "float",   // GANGLIA_VALUE_FLOAT
    "double"   // GANGLIA_VALUE_DOUBLE
};

```


## The Protocol ##

| Index | Format            | Notes|
|:------|:------------------|:-----|
| 1     | xdr\_enum(0)       | 0 stands for gmetric |
| 2     | xdr\_string(type)  |  The appropriate string from `typestrings` is used instead |
| 3     | xdr\_string(name)  | Arbitrary string |
| 4     | xdr\_string(value) | Binary XDR encoding is _not_ used |
| 5     | xdr\_string(units) | Arbitrary string |
| 6     | xdr\_enum(slope)   | See slope bug below |
| 7     | xdr\_u\_int(tmax)   |  |
| 8     | xdr\_u\_int(dmax)   |  |


### slope bug ###

All versions of gmetric and gmond <= 3.0.4 have a bug.

Gmetric (the command line application) will only send a slope of type "0" (zero) or type "3" (both).

Gmond when printing XML data, will only print "zero" or "both" for the slope.  Meaning if you send a slope of "1", (positive), gmond will print "both".


This is fixed on mainline, I believe to be released as 3.1
