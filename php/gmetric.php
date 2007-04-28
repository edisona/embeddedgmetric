#!/usr/bin/env php
<?php

function xdr_uint32($val)
{
    return pack("N", intval($val));
}

function xdr_string($str)
{
    $len = strlen(strval($str));
    $pad = (4 - $len % 4) % 4;
    return xdr_uint32($len) . $str . pack("a$pad", "");
}

function makexdr($name, $value, $typename, $units, $slope, $tmax, $dmax)
{

    if ($slope == "zero") {
        $slopenum = 0;
    } else if ($slope == "positive") {
        $slopenum = 1;
    } else if ($slope == "negative") {
        $slopenum = 2;
    } else if ($slope == "both") {
        $slopenum = 3;
    } else {
        $slopenum = 4;
    }

    $str  = xdr_uint32(0);
    $str .= xdr_string($typename);
    $str .= xdr_string($name);
    $str .= xdr_string($value);
    $str .= xdr_string($units);
    $str .= xdr_uint32($slopenum);
    $str .= xdr_uint32($tmax);
    $str .= xdr_uint32($dmax);
    return $str;
}

function gmetric_open($host, $post, $proto)
{
    if ($proto == "udp") {
        $fp = fsockopen("udp://$host", $port, $errno, $errstr);
        return array('protocol' => $proto,
                     'socket' => $fp);
    } else if ($proto == "multicast") {
        return array('protocol' => 'not supported');

        // the code should look something like this however

        $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
        if ($sock === false) {
            echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
        }
        $address = gethostbyname($host);
        $result = socket_connect($sock, $address, $port);
        if ($result === false) {
            echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
        }

        /**
         ** MUTLICAST SOCKET OPTIONS GO HERE
         ** http://devzone.zend.com/node/view/id/1432
         ** http://diary.rozsnyo.com/2006/06/16/php-multicast/
         **/

        return array('protocol' => $proto,
                     'socket' => $sock);
    } else {
        // unknown!
    }
}

function gmetric_send($gm, $name, $value, $typename, $units, $slope, $tmax, $dmax)
{
    $msg  = makexdr($name, $value, $typename, $units, $slope, $tmax, $dmax);
    if ($gm['protocol'] == 'udp') {
        return fwrite($gm['socket'], $msg);
    } else if ($gm['protocol'] == 'mutlicast') {
        return socket_write($gm['socket'], $msg, strlen($msg));
    } else {
        return false;
    }
}

function gmetric_close($gm)
{
    if ($gm['protocol'] == 'udp') {
        return fclose($gm['socket']);
    } else if ($gm['protocol'] == 'multicast') {
        return socket_close($gm);
    }
}

/*
$msg = makexdr("foo", "bar", "string", "", "both", 60, 0);
$foo = "0000000000000006737472696e67000000000003666f6f00000000036261720000000000000000030000003c00000000";
$str = gmetric("foo", "bar", "string", "", "both", 60, 0);
echo strlen($str);
echo "\n";
$result =  bin2hex($str);
if ($foo == $result) {
  echo "match\n";
} else {
  echo "BAD\n";
  echo "$foo\n";
  echo "$result\n";
}*/

?>