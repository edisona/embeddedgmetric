#!/usr/bin/env python

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

import xdrlib
import socket

class Gmetric:
    slope = {'zero':0, 'positive':1, 'negative':2, 'both':3, 'unspecified':4}
    type = ('', 'string', 'uint16', 'int16', 'uint32', 'int32', 'float', 'double', 'timestamp')
    protocol = ('udp', 'multicast')

    def __init__(self, host, port, protocol):
        if protocol not in self.protocol:
            raise ValueError("Protocol must be one of: " + str(self.protocol))
        self.msg = xdrlib.Packer()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if protocol == 'multicast':
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        self.hostport = (host, int(port))
        #self.socket.connect(self.hostport)

    def send(self, name, value, typestr='', unitstr='', slopestr='both', tmax=60, dmax=0):
        msg = self.makexdr(name, value, typestr, unitstr, slopestr, tmax, dmax)
        return self.socket.sendto(msg, self.hostport)
                     
    def makexdr(self, name, value, typestr, unitstr, slopestr, tmax, dmax):
        #
        # socket free code to aid in testing
        #
        if slopestr not in self.slope:
            raise ValueError("Slope must be one of: " + str(self.slope.keys()))
        if typestr not in self.type:
            raise ValueError("Type must be one of: " + str(self.type))
        if len(name) == 0:
            raise ValueError("Name must be non-empty")

        self.msg.reset()
        self.msg.pack_int(0)   # type gmetric
        self.msg.pack_string(typestr)
        self.msg.pack_string(name)
        self.msg.pack_string(str(value))
        self.msg.pack_string(unitstr)
        self.msg.pack_int(self.slope[slopestr]) # map slope string to int
        self.msg.pack_uint(int(tmax))
        self.msg.pack_uint(int(dmax))
        return self.msg.get_buffer()

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("", "--protocol", dest="protocol", default="udp",
                      help="The gmetric internet protocol, either udp or multicast, default udp")
    parser.add_option("", "--host",  dest="host",  default="127.0.0.1",
                      help="The gmond host to recieve the data")
    parser.add_option("", "--port",  dest="port",  default="8649",
                      help="The gmond port to recieve the data")
    parser.add_option("", "--name",  dest="name",  default="",
                      help="The name of the metric")
    parser.add_option("", "--value", dest="value", default="",
                      help="The value of the metric")
    parser.add_option("", "--units", dest="units", default="",
                      help="The units for the value, e.g. 'kb/sec'")
    parser.add_option("", "--slope", dest="slope", default="both",
                      help="The sign of the derivative of the value over time, one of zero, positive, negative, both, default both")
    parser.add_option("", "--type",  dest="type",  default="",
                      help="The value data type, one of string, int8, uint8, int16, uint16, int32, uint32, float, double")
    parser.add_option("", "--tmax",  dest="tmax",  default="60",
                      help="The maximum time in seconds between gmetric calls, default 60")
    parser.add_option("", "--dmax",  dest="dmax",  default="0",
                      help="The lifetime in seconds of this metric, default=0, meaning unlimited")
    (options,args) = parser.parse_args()

    g = Gmetric(options.host, options.port, options.protocol)
    g.send(options.name, options.value, options.type, options.units,
           options.slope, options.tmax, options.dmax)
