## Simple Usage ##
This creates and sends a single metric.

```
/* create the gmetric, this only needs to be done once in the app */
gmetric g;                                                                                                                                                                                                                                        
gmetric_create(&g);                                                                                                                  
if (!gmetric_open(g, 'localhost', 8649)) {
    /* ERROR */                                                                                                                     
}

/* generate the message and send */
gmetric_message msg;
gmetric_message_clear(&msg);
msg.type = GMETRIC_VALUE_STRING;
msg.name = 'foo';
msg.value.v_string = 'bar';
msg.units ='units!'
msg.slope = GMETRIC_SLOPE_ZERO;
msg.tmax = 60;
msg.dmax = 0;
if (gmetric_send(&g, &msg) == -1) {
    /* ERROR */
}

/* cleanup */
gmetric_close(&g);
```

If you had a double value and not a string, you would just change
```
msg.type = GMETRIC_VALUE_DOUBLE;
msg.value.v_double = 1.2345;
msg.slope = GMETRIC_SLOPE_BOTH;
```

etc.

## Bulk Usage ##

If you need to send many message, or send the same message to more than one destination, you can optimize the code by recycling buffers.


```
/* create the gmetric, this only needs to be done once in the app */
gmetric g;                                                                                                                                                                                                                                        
gmetric_create(&g);                                                                                                                  
if (!gmetric_open(g, 'localhost', 8649)) {
    exit(1);                                
}

/* make buffers */
gmetric_message msg;
char buf[MAX_GMETRIC_MESSAGE];

foreach metric {
    gmetric_message_clear(&msg);
    msg.type = GMETRIC_VALUE_STRING;
    msg.name = 'foo';
    msg.value.v_string = 'bar';
    msg.unit = 'no units';
    msg.slope = GMETRIC_SLOPE_BOTH;
    msg.tmax = 120;
    msg.dmax = 0;

    int len = gmetric_message_create_xdr(buf, sizeof(buf), &msg);
    if (len == -1) {
        continue; /* ERROR */
    }
    gmetric_send_xdr(&g, buf, len);
}

/* cleanup */
gmetric_close(&g);
```

## Notes ##

This version coverts the metric value (e.g. 'int', 'double') to a string (required by protocol) _without_ using `sprintf` (or related functions).

See [here](http://code.google.com/p/stringencoders/wiki/NumToA) for details.  Besides making `embeddedgmetric` even faster, it also makes it more portable and is safer (e.g. no more buffer overflows, core dumps, etc).