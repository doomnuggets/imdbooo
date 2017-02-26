#!/bin/bash

# Remove python cache files.
find lib/ -type f -name '*.pyc' -delete
rm -f *.pyc
