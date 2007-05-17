
.PHONY: clean distclean

if PYTHON
all:
	python setup.py build


clean:
	rm -f *.pyc *~
	python setup.py clean
	rm -rf build

distclean: clean

install:
	python setup.py install

uninstall:
	python setup.py uninstall
else

# do nothing if python not requested

all:

clean:

distclean:

test:

install:

uninstall:

endif

