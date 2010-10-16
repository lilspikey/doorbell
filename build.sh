#!/bin/sh

# copy files to dist directory
# for installing on chumby
if [ ! -d dist/gntp ]; then
    mkdir -p dist/gntp
fi
cp debugchumby *.py dist
cp src/gntp/gntp/*.py dist/gntp
