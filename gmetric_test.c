/* -*- mode: c; c-basic-offset: 4; indent-tabs-mode: nil; tab-width: 4 -*- */
/* vi: set expandtab shiftwidth=4 tabstop=4: */
/* RMHEADER
 */

#include "embeddedgmetric.h"
#include <stdio.h>

int gErrors = 0;

#define TS_ASSERT(A) if (!(A)) { printf("%d:%s assertion failed\n", __LINE__, __FILE__); gErrors++;}

void testCreate()
{
    char buffer[GMETRIC_MAX_MESSAGE_LEN];
    gmetric_message_t msg;
	msg.type = GMETRIC_VALUE_STRING;
	msg.name ="foo";
	msg.value.v_string = "bar";
    msg.typestr = 0;
    msg.units = "";
	msg.slope = GMETRIC_SLOPE_ZERO;
	msg.tmax = 60;
	msg.dmax = 0;

    int len = gmetric_message_create_xdr(buffer, sizeof(buffer), &msg);
#if 0
    printf("\nMSG LEN: %d\n", len);
	int i = 0;
    for (i = 0; i < len; ++i) {
        printf("%02x", (unsigned char)(buffer[i]));
    }
    printf("%s", "\n");
#endif
    TS_ASSERT(48 == len);
}

/** \brief Make a message and actually send it.
 *
 */
void testSend()
{
    gmetric_message_t msg;
	msg.type = GMETRIC_VALUE_STRING;
    /* 	msg.type = GMETRIC_VALUE_DOUBLE; */
 	msg.name ="foo";
	msg.value.v_string = "bar";
    /* msg.value.v_double = 1.2345; */
    msg.typestr = 0;
    msg.units = "";
	msg.slope = GMETRIC_SLOPE_ZERO;
	msg.tmax = 60;
	msg.dmax = 0;

    gmetric_t g;
    gmetric_create(&g);
    TS_ASSERT(gmetric_open(&g, "127.0.0.1", 8649));
    TS_ASSERT(48 == gmetric_send(&g, &msg));
    gmetric_close(&g);
}

/** \brief test bad host
 *
 */
void testSendBadHost()
{
    gmetric_t g;
    gmetric_create(&g);
    TS_ASSERT(!gmetric_open(&g, "xxx.qq.zzz", 8649));
}

/** \brief Test using a bogus port
 *
 * for some reason this WORKS (??)
 */
void testSendBadPort()
{
    gmetric_t g;
    gmetric_create(&g);
    TS_ASSERT(gmetric_open(&g, "localhost", 198649));
}

/** \brief test that 'localhost' and '127.0.0.1' work
 *
 */
void testSendLocalhost()
{
    gmetric_t g;
    gmetric_create(&g);
    TS_ASSERT(gmetric_open(&g, "localhost", 8649));
    TS_ASSERT(gmetric_open(&g, "127.0.0.1", 8649));
}

int main()
{
    testCreate();
    testSend();
    testSendBadPort();
    testSendLocalhost();
    return gErrors;
}
