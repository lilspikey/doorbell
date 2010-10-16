#!/bin/sh

# copy files to dist directory
# for installing on chumby
# assumes dependencies are installed
# into virtualenv within current directory.
# including all dependencies to simply "installing"
# on chumby
if [ ! -d dist/gntp ]; then
    mkdir -p dist/gntp
fi
if [ ! -d dist/serial ]; then
    mkdir -p dist/serial
fi
cp debugchumby *.py dist
cp src/gntp/gntp/*.py dist/gntp
cp lib/python2*/site-packages/serial/*.py dist/serial
