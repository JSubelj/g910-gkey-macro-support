#!/usr/bin/env bash


python3 setup.py install --record files.txt
cp g910-gkey-macro-support /etc/init.d/g910-gkey-macro-support
