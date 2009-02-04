#!/usr/bin/env python

#
# SUPER LOW LEVEL WEBSERVER
# Sorta like CGI if anyone remembers that
#
#
from wsgiref.simple_server import make_server
from wsgiref.util import FileWrapper
import cgi

import qparse

static_root = '.'
rrd_root = '/tmp'

def sendfile(fname, start_response):
    status =  "200 OK"
    mtype = 'text/plain'
    try:
        f = open(filename, 'r'); data = f.read(); f.close()
        m = mimetypes.guess_type(filename)
        if m[0] is not None: mtype = m[0]
    except IOError,e:
        data = str(e) + '\n'
        status = "404 Not Found"
    start_response(status, [('Content-Type', mtype)])
    return [ data ]

def static(environ, start_response):
    # shift PATH_INFO /static/foo ----> /foo
    # then skip first '/'
    # and merge with static_root
    wsgiref.util.shift_path_info(environ)
    filename = os.path.abspath(os.path.join(static_root,
                                            environ['PATH_INFO'][1:]))
    return sendfile(fname, start_response)

def rrd(environ, start_response):
    wsgiref.util.shift_path_info(environ)
    filename = os.path.abspath(os.path.join(static_root,
                                            environ['PATH_INFO'][1:]))
    qs = cgi.parse_qs(environ['QUERY_STRING'])
    host = qs['host'][0]
    metric = qs['metric'][0]
    duration = qs['duration'][0]
    
    # optional
    width = 400
    if 'width' in qs:
        width = int(qs['width'][0])
    
    return sendfile(fname, start_response)

# just for debugging
def echo(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    text = []
    keys = sorted(environ.keys())
    for k in keys:
        text.append("%s = %s\n" % (k,environ[k]))
    return text

def dispatch(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/echo':
        return echo(environ, start_response)
    if path == '/rrd':
        return rrd(environ, start_response)

    # remap common webby things into the static directory
    if path == '/favicon.txt' or path == '/robots.txt':
        path = '/static' + path
        environ['PATH_INFO'] = path
    if path.startswith('/static'):
        return static(environ, start_response)

    # nothing matched, do 404
    status = "404 Not Found"
    start_response(status, [('Content-Type', 'text/plain')])
    return [ "%s not found" % path ]


if __name__ == '__main__':
    httpd = make_server('', 8000, dispatch)
    print "Serving on port 8000..."

    # Serve until process is killed
    httpd.serve_forever()
