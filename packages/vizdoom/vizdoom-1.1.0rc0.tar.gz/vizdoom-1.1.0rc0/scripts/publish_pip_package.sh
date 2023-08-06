#!/usr/bin/env bash

python setup.py sdist
twine register `ls dist/* | sort | tail -n 1`


