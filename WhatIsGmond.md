Gmond is a interesting service.   Oddly there isn't much of a "systems overview"  on [Ganglia](http://ganglia.info) website, and reading the [documentation](http://sourceforge.net/docman/display_doc.php?docid=128913&group_id=43021) may leave you scratching your head.

It does a few things:

  * collects machine metrics (cpu, load, bytes in/out, disk space, etc)...
  * send metrics to "the mothership" or to every other machine running gmond via multicast
  * receive metrics from other machines
  * manages metrics, expiring old, stale entries.
  * exporting metrics into XML format

If this sounds a bit confused, there is a method to the madness and it allows all sorts of interesting configuration (most of which may not be interesting to you, but they are possible).

(Oh yeah, this is "embedded gmetric", let me say what 'gmetric' is.  It's a tool for directly injecting new metrics into gmond).

I think of gmond as a collection of subsystems I calls: the tree, the reader, the writer, the collector and emiter.

## The Tree ##

The internal data structure of gmond is a tree.

  1. Gmond is basically a tree, which can be implemented as a series of hash tables (cluster/machine/metric name/metric metadata).
  1. Each metric (or node) has an expiration date.  If a node is past the expiration date, it is deleted.
  1. There are some other minor details but that's about it

## The Reader ##

The collector sits on a socket and reads UDP or multicast packets of metrics data.  The API here is a XDR encoded "packet" and it's small, typically under 100 bytes.   XDR encoding is really simple and most scripting languages and operating systems provide a library for it.

## The Writer ##

The writer listens on a different socket, and when _any_ request comes in, it serialize the tree into a XML format.

## Collector ##

The collector, guess what, collects metrics on periodic basis.  The `gmond` implementation typically uses direct system calls and has many modules that do the right thing for different operating system types.   But even with direct system calls, a good bit of string processing might be needed.

## Emitter ##

Interestingly, the collector does _not_ put it's stats into the internal tree.    Instead it "emits"  the metric in XDR format as  UDP or multicast packets.  It might be the same local machine or it might be another machine.

It may be that gmond does an optimization, where if the emitter it sending to the localhost, it just does a direct insert to the tree.

## Other Stuff ##

of course there is code to parse config and command lines

# Implementation #

The  tree/reader/writer and collector/emitter could be completely separated and talk via XDR packets.  However then  one would need _two_ daemons running.  That would suck, so they are merged into one.  But logically they are distinct.