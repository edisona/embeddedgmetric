#!/usr/bin/env perl

use strict;
use IO::Socket::INET;

sub xdr_uint32($)
{
    my $val = shift;
    return pack 'N', int($val);
}

sub xdr_string($)
{
    my $str = shift;
    my $len = length $str;
    my $pad = (4 - $len % 4) % 4;
    return xdr_uint32($len) . $str . pack "a$pad", '';
}

sub makexdr($$$$$$$)
{
    my ($name, $value, $typename, $units, $slope, $tmax, $dmax) = @_;

    my $slopenum;
    if ($slope == "zero") {
        $slopenum = 0;
    } elsif ($slope == "positive") {
        $slopenum = 1;
    } elsif ($slope == "negative") {
        $slopenum = 2;
    } elsif ($slope == "both") {
        $slopenum = 3;
    } else {
        $slopenum = 4;
    }

    my $str  = xdr_uint32(0);
    $str .= xdr_string($typename);
    $str .= xdr_string($name);
    $str .= xdr_string($value);
    $str .= xdr_string($units);
    $str .= xdr_uint32($slopenum);
    $str .= xdr_uint32($tmax);
    $str .= xdr_uint32($dmax);
    return $str;
}

sub gmetric_open($$$)
{
    my ($host, $port, $proto) = $@;

    my $sock = IO::Socket::INET->new(PeerAddr => $host,
				     PeerPort => $port,
				     Proto    => 'udp');
}

sub gmetric_send($$$$$$$$)
{
    my ($sock, $name, $value, $typename, $units, $slope, $tmax, $dmax) = @_;

    my $msg  = makexdr($name, $value, $typename, $units, $slope, $tmax, $dmax);
    $sock->send($msg);
}

sub gmetric_close($)
{
    my $sock = shift;
    $sock->close();
}

sub binhex ($)
{
    my $str = shift;
    $str =~ s/(.|\n)/sprintf("%02lx", ord $1)/eg;
    return $str;
}

my $msg = makexdr('foo', 'bar', 'string', '', 'both', 60, 0);
print length $msg;
print "\n";

print binhex($msg);
print "\n";
print hex $msg;