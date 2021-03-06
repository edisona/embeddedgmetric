

/*
 * This is the MIT License
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright (c) 2009 Nick Galbreath
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

import java.io.DataOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

/**
 *
 *
 *
 */
class gmetric {

    public final static int SLOPE_ZERO         = 0;
    public final static int SLOPE_POSITIVE     = 1;
    public final static int SLOPE_NEGATIVE     = 2;
    public final static int SLOPE_BOTH         = 3;
    public final static int SLOPE_UNSPECIFIED  = 4;

    public final static String VALUE_STRING          = "string";
    public final static String VALUE_UNSIGNED_SHORT  = "uint16";
    public final static String VALUE_SHORT           = "int16";
    public final static String VALUE_UNSIGNED_INT    = "uint32";
    public final static String VALUE_INT             = "int32";
    public final static String VALUE_FLOAT           = "float";
    public final static String VALUE_DOUBLE          = "double";

    public static void send(InetAddress address, int port,
			    String name, String value, String type,
			    String units, int slope, int tmax, int dmax)
    {
	try {
	    DatagramSocket socket = new DatagramSocket();
	    byte[] buf = write(name, value, type, units, slope, tmax, dmax);
	    DatagramPacket p = new DatagramPacket(buf, buf.length, address, port);
	    socket.send(p);
	} catch (IOException e) {
	    // who cares
	}
    }

    public static void send(InetAddress address, int port,
			    String name, double dvalue,
			    String units, int slope, int tmax, int dmax)
    {
	try {
	    String value = Double.toString(dvalue);
	    DatagramSocket socket = new DatagramSocket();
	    byte[] buf = write(name, value, VALUE_DOUBLE, units, slope, tmax, dmax);
	    DatagramPacket p = new DatagramPacket(buf, buf.length, address, port);
	    socket.send(p);
	} catch (IOException e) {
	    // who cares
	}
    }

    public static void send(InetAddress address, int port,
			    String name, int dvalue,
			    String units, int slope, int tmax, int dmax)
    {
	try {
	    String value = Integer.toString(dvalue);
	    DatagramSocket socket = new DatagramSocket();
	    byte[] buf = write(name, value, VALUE_INT, units, slope, tmax, dmax);
	    DatagramPacket p = new DatagramPacket(buf, buf.length, address, port);
	    socket.send(p);
	} catch (IOException e) {
	    // who cares
	}
    }



    /*
     * EVERYTHING BELOW HERE YOU DON"T NEED TO USE
     */

    public static byte[] write(String name, String value, String type,
			       String units, int slope, int tmax, int dmax)
    {
	try {
	    ByteArrayOutputStream baos = new ByteArrayOutputStream();
	    DataOutputStream dos = new DataOutputStream(baos);
	    dos.writeInt(0);
	    writeXDRString(dos, type);
	    writeXDRString(dos, name);
	    writeXDRString(dos, value);
	    writeXDRString(dos, units);
	    dos.writeInt(slope);
	    dos.writeInt(tmax);
	    dos.writeInt(dmax);
	    return baos.toByteArray();
	} catch (IOException e) {
	    // really this is impossible
	    return null;
	}
    }

    private static void writeXDRString(DataOutputStream dos, String s) throws IOException
    {
	dos.writeInt(s.length());
	dos.writeBytes(s);
	int offset = s.length() % 4;
	if (offset != 0) {
	    for (int i = offset; i < 4; ++i) {
		dos.writeByte(0);
	    }
	}
	/*
	bytes[] b = s.getBytes("utf8");
	int len = b.length();
	dos.writeInt(len);
	dos.write(b, 0, len);
	*/
    }

    /*
     * Everything below here is just for testing
     */
    private static final byte[] HEXCHARS = {
	(byte)'0', (byte)'1', (byte)'2', (byte)'3',
	(byte)'4', (byte)'5', (byte)'6', (byte)'7',
	(byte)'8', (byte)'9', (byte)'a', (byte)'b',
	(byte)'c', (byte)'d', (byte)'e', (byte)'f'
    };

    private static String bytes2hex(byte[] raw)
    {
	try {
	    int pos = 0;
	    byte[] hex = new byte[2 * raw.length];
	    for (int i = 0; i < raw.length; ++i) {
		int v = raw[i] & 0xFF;
		hex[pos++] = HEXCHARS[v >>> 4];
		hex[pos++] = HEXCHARS[v & 0xF];
	    }

	    return new String(hex, "ASCII");
	} catch (UnsupportedEncodingException e) {
	    // impossible
	    return "";
	}
    }

    public static void selfTest()
    {
	String expected = "0000000000000006737472696e67000000000003666f6f00000000036261720000000000000000030000003c00000000";
	byte[] data = write("foo", "bar", VALUE_STRING, "", SLOPE_BOTH, 60, 0);
	String result = bytes2hex(data);
	if (!expected.equals(result)) {
	    System.out.println(expected);
	    System.out.println(result);
	    throw new RuntimeException("bad");
	}
    }

    public static void main(String args[]) throws Exception {
	selfTest();
    }
}
