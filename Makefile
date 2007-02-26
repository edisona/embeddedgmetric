
foo: embeddedgmetric.c embeddedgmetric.c
	${CC} -o gmetric -Wall -O3 embeddedgmetric.c

gtest: embeddedgmetric.c embeddedgmetric.c gmetric_test.c
	${CC} -o gtest -Wall -O3 embeddedgmetric.c gmetric_test.c