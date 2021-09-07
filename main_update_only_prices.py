#!/usr/bin/python

bundle_main = "bundle_main"

from bundle_main import checks
print('0 checks - done')

print('prices_updated - initiating. Printing Stock and % Progress.')
from bundle_main import prices_update
print('prices_updated - done')

print('prices_combine - initiating.')
from bundle_main import prices_process
print('prices_combine - done')

print('datasets_merge - initiating.')
from bundle_main import datasets_merge
print('datasets_merge - done')

from bundle_main import output
print('output - done')


