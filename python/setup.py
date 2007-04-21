
#
# This don't do much.. the module is just 1 file
#
from distutils.core import setup
setup(name='gmetric',
      version='1.0',
      author='Nick Galbreath',
      author_email='nickg [at] modp [dot] com',
      description='library and cmd-line to inject statistics into gmond.  See http://ganglia.info',
      url='http://code.google.com/p/embeddedgmetric/',
      py_modules=['gmetric'],
      )
