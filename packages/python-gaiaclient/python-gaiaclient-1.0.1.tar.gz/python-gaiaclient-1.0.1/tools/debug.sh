#!/usr/bin/env bash

source .tox/py27/bin/activate
testr list-tests $1 > .debug; python -m testtools.run discover --load-list .debug
