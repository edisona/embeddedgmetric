
foo: embeddedgmetric.c embeddedgmetric.c
	${CC} -o gmetric -Wall -g embeddedgmetric.c

gtest: embeddedgmetric.c embeddedgmetric.c gmetric_test.c
	${CC} -o gtest -Wall -g embeddedgmetric.c gmetric_test.c