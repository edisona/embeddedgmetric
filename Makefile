

all: gtest

gtest: embeddedgmetric.c embeddedgmetric.c gmetric_test.c
	${CC} -o gtest -Wall -g embeddedgmetric.c gmetric_test.c

.PHONY: test clean
test: gtest
	./gtest
	python/gmetric_test.py
clean:
	rm -rf gtest
	find . -name '*~' | xargs rm -f
	find . -name '*.pyc' | xargs rm -f
