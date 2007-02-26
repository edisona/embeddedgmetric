/* -*- mode: c; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */

/**
 * This is the MIT LICENSE
 *
 * Copyright (c) 2007 Nick Galbreath
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include "embeddedgmetric.h"
#include <stdio.h>
#include <netdb.h>
#include <rpc/rpc.h>
#include <unistd.h>
#include <string.h>

#define CONVERT_TO_STRINGS

static const char* typestrings[] = {
    "", "string", "uint16", "int16", "uint32", "int32", "float", "double"
};

int gmetric_message_create_xdr(char* buffer, uint len,
                               const gmetric_message_t* msg)
{

    XDR x;
    xdrmem_create(&x, buffer, len, XDR_ENCODE);

#ifdef CONVERT_TO_STRINGS
    char valbuf[64];
    char* valbufptr = valbuf;

    enum_t tmp = 0;
    if (!xdr_enum (&x, (enum_t*) &tmp)) {
        return -1;
    }
#else
    if (!xdr_enum (&x, (enum_t*) &msg->type)) {
        return -1;
    }
#endif

    const char* typestr = typestrings[msg->type];
    if (msg->typestr && msg->typestr[0] != 0) {
        typestr = msg->typestr;
    }
    if (!xdr_string(&x, (char**) &typestr, ~0)) {
        return -1;
    }

    if (!xdr_string(&x, (char**) &msg->name, ~0)) {
        return -1;
    }

    switch (msg->type) {
    case GANGLIA_VALUE_UNSIGNED_SHORT:
#ifdef CONVERT_TO_STRINGS
        snprintf(valbuf, sizeof(valbuf), "%hu", msg->value.v_ushort);
        if (!xdr_string(&x, &valbufptr, sizeof(valbuf))) {
            return -1;
        }
#else
        if (!xdr_u_short(&x, (unsigned short*) &msg->value.v_ushort)) {
            return -1;
        }
#endif
        break;
    case GANGLIA_VALUE_SHORT:
#ifdef CONVERT_TO_STRINGS
        snprintf(valbuf, sizeof(valbuf), "%hd", msg->value.v_ushort);
        if (!xdr_string(&x, &valbufptr, sizeof(valbuf))) {
            return -1;
        }
#else
        if (!xdr_short(&x, (short*) &msg->value.v_short)) {
            return -1;
        }
#endif
        break;
    case GANGLIA_VALUE_UNSIGNED_INT:
#ifdef CONVERT_TO_STRINGS
        snprintf(valbuf, sizeof(valbuf), "%u", msg->value.v_uint);
        if (!xdr_string(&x,  &valbufptr, sizeof(valbuf))) {
            return -1;
        }
#else
        if (!xdr_u_int(&x, (unsigned int*) &msg->value.v_uint)) {
            return -1;
        }
#endif
        break;
    case GANGLIA_VALUE_INT:
#ifdef CONVERT_TO_STRINGS
        snprintf(valbuf, sizeof(valbuf), "%d", msg->value.v_int);
        if (!xdr_string(&x, &valbufptr, sizeof(valbuf))) {
            return -1;
        }
#else
        if (!xdr_int(&x, (int*) &msg->value.v_int)) {
            return -1;
        }
#endif
        break;
    case GANGLIA_VALUE_FLOAT:
#ifdef CONVERT_TO_STRINGS
        snprintf(valbuf, sizeof(valbuf), "%f", msg->value.v_float);
        if (!xdr_string(&x,  &valbufptr, sizeof(valbuf))) {
            return -1;
        }
#else
        if (!xdr_float(&x, (float*) &msg->value.v_float)) {
            return -1;
        }
#endif
        break;
    case GANGLIA_VALUE_DOUBLE:
#ifdef CONVERT_TO_STRINGS
        snprintf(valbuf, sizeof(valbuf), "%f", msg->value.v_double);
        if (!xdr_string(&x, &valbufptr, sizeof(valbuf))) {
            printf("DOUBLE\n");
            return -1;
        }
#else
        if (!xdr_double(&x, (double*) &msg->value.v_double)) {
            return -1;
        }
#endif
        break;
    case GANGLIA_VALUE_STRING:
        //printf("STRING: %s\n", msg->value.v_string);
        if (!xdr_string(&x, (char**) &msg->value.v_string, ~0)) {
            return -1;
        }
        break;
    case GANGLIA_VALUE_UNKNOWN:
        if (!xdr_string(&x, (char**) &msg->value.v_string, ~0)) {
            return -1;
        }
        break;
    }  /* end switch */

    if (!xdr_string(&x, (char**) &msg->units, ~0)) {
        return -1;
    }

    if (!xdr_u_int(&x, (u_int*) &msg->slope)) {
        return -1;
    }

    if (!xdr_u_int(&x, (u_int*) &msg->tmax)) {
        return -1;
    }

    if (!xdr_u_int(&x, (u_int*) &msg->dmax)) {
        return -1;
    }

    return xdr_getpos(&x);
}

/**
 * "constructor"
 */
void gmetric_create(gmetric_t* g)
{
    /* zero out everything
     * and set socket to invalid
     */
    memset(g, 0, sizeof(gmetric_t));
    g->s = -1;
}

/**
 * open up a socket
 */
int gmetric_open(gmetric_t* g, const char* addr, int port)
{
    if (g->s == -1) {
        gmetric_close(g);
    }
    g->s = -1;
    g->s = socket(AF_INET, SOCK_DGRAM,  IPPROTO_UDP);
    if (g->s == -1) {
        return 0;
    }

    memset(&g->sa, 0, sizeof(struct sockaddr_in));
    g->sa.sin_family = AF_INET;
    g->sa.sin_port = htons(port);

    struct hostent* result = NULL;
#if 0
    /* super annoying thread safe version */
    struct hostent he;
    char tmpbuf[1024];
    int local_errno = 0;
    if (gethostbyname_r(addr, &he, tmpbuf, sizeof(tmpbuf),
                        &result, &local_errno)) {
        gmetric_close(g);
        return 0;
    }
#else
    /* thread un-safe?? */
    result = gethostbyname(addr);
#endif

    if (result == NULL) {
        gmetric_close(g);
        return 0;
    }
    memcpy(&g->sa.sin_addr, result->h_addr_list[0], result->h_length);

    return 1;
}

int gmetric_send_xdr(gmetric_t* g, const char* buf, int len)
{
    return sendto(g->s, (char*)buf, len, 0,
                  (struct sockaddr*)&g->sa, sizeof(struct sockaddr_in));
}

int gmetric_send(gmetric_t* g, const gmetric_message_t* msg)
{
    char buf[GANGLIA_MAX_MESSAGE_LEN];
    int len = gmetric_message_create_xdr(buf, sizeof(buf), msg);
    return gmetric_send_xdr(g, buf, len);
}

/**
 * "destructor"
 */
void gmetric_close(gmetric_t* g)
{
    if (g->s != -1) {
        close(g->s);
    }
    g->s = -1;
}

void gmetric_message_clear(gmetric_message_t* msg)
{
    msg->type = GANGLIA_VALUE_UNKNOWN;
    msg->name = "";
    msg->units = "";
    msg->typestr = "";
    msg->slope = 0;
    msg->tmax = 60;
    msg->dmax = 0;
    msg->value.v_double = 0;
}
