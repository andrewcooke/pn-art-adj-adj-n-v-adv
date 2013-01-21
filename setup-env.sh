#!/bin/bash

rm -fr env
virtualenv --python=python3.2 env
source env/bin/activate
easy_install pycrypto
easy_install brigit
easy_install twitter
