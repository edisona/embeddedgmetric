Hi there, good news, bad news.



## The good news ##

I just checked in [php/gmetric.php](http://embeddedgmetric.googlecode.com/svn/trunk/php/gmetric.php) -- it's a pure php4/php5 version of gmetric.

```
$gm = gmetric_open('localhost', 8649, 'udp');
gmetric_send($gm, 'foo', 'bar', 'string', 'both', '', 60, 60);
// as many other gmetric_sends as you want
gmetric_close($gm);
```

## The Bad News ##

The bad new is that I'm not a php expert.

mutlicast is _not_ supported since php doesn't support the raw socket options that are required.  boo.  However I more or less mapped out what would need to be done.  Also the ext/socket library is set to move to an extension starting in 5.3 (not released, no idea what or when).

So the udp options uses raw fsockopen, fwrite, fclose which should work in all versions.


Oh yeah, more bad news.  It's not tested yet.

## HELP WANTED ##

I'm not a php expert. Any help/advice on packaging, making it OO, etc would be welcome!