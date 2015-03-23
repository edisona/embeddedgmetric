# Gmetric Perl #

Yet another implementation of the gmetric protocol, this time in perl.

Check out [perl/gmetric.pl](http://embeddedgmetric.googlecode.com/svn/trunk/perl/gmetric.pl)

THIS IS ALPHA

It "works" but it's not pretty yet.


## Usage ##

A little something like this:

```
my $gm = gmetric_open('localhost', 8649, 'udp');
gmetric_send($gm, 'foo', 'bar', 'string', '', 'both', 60, 60);
gmetric_close($gm);
```

## Multicast ##

TO DO.  I'll need to pull in another module to do this.  I think.

## HELP WANTED ##

I'm not a perl expert.  Any help/advice on packaging, making it OO, etc would be welcome!