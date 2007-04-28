#!/usr/bin/env perl

# This is the MIT License
# http://www.opensource.org/licenses/mit-license.php
#
# Copyright (c) 2007 Nick Galbreath
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

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
    my ($host, $port, $proto) = @_;
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

sub binhex($)
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

my $gm = gmetric_open('localhost', 8649, 'udp');
gmetric_send($gm, 'foo', 'bar', 'string', '', 'both', 60, 60);
gmetric_close($gm);

