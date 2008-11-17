#!/bin/sh

FILE=embeddedgmetric-v1.3.0
rm -rf ${FILE}
svn export http://embeddedgmetric.googlecode.com/svn/trunk ${FILE}

find $FILE -name '.svn' | xargs rm -rf

# don't package pmond for now
rm -rf pmond

rm -f ${FILE}/makerelease.sh
rm -f ${FILE}.tar.gz
tar -czvf ${FILE}.tar.gz ${FILE}
rm -rf ${FILE}
echo "DONE"
ls -lh ${FILE}.tar.gz
