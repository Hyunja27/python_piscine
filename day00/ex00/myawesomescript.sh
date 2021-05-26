#!/bin/sh

if [ $1 ] ; then
    curl -s $1 | grep body | cut -d\" -f2
fi
