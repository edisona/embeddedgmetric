

all: gtest

gtest: embeddedgmetric.c embeddedgmetric.c gmetric_test.c
	${CC} -o gtest -Wall -g embeddedgmetric.c gmetric_test.c

clean:
	rm -rf gtest
	find . -name '*~' | xargs rm -f
	find . -name '*.pyc' | xargs rm -f
