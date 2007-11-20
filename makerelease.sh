#!/bin/sh

FILE=embeddedgmetric-v1.2.0
rm -rf ${FILE}
svn export http://embeddedgmetric.googlecode.com/svn/trunk ${FILE}

find $FILE -name '.svn' | xargs rm -rf

rm -f ${FILE}/makerelease.sh
rm -f ${FILE}.tar.gz
tar -czvf ${FILE}.tar.gz ${FILE}
rm -rf ${FILE}
echo "DONE"
ls -lh ${FILE}.tar.gz
