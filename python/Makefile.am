
all:
	python setup.py build

.PHONY: clean distclean

clean:
	rm -f *.pyc *~
	python setup.py clean
	rm -rf build

distclean: clean

install:
	python setup.py install

uninstall:
	python setup.py uninstall
