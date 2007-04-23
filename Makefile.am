


lib_LTLIBRARIES = libembeddedgmetric.la
libembeddedgmetric_la_SOURCES = src/embeddedgmetric.c src/modp_numtoa.c
include_HEADERS = src/embeddedgmetric.h

noinst_PROGRAMS = gtest
gtest_SOURCES = gmetric_test.c
gtest_LDADD = libembeddedgmetric.la

.PHONY: test

test: gtest
	./gtest
	python/gmetric_test.py

CLEANFILE: gtest *~ python/*~ python/*.pyc
