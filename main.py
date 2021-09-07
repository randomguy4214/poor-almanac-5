#!/usr/bin/python

bundle_main = "bundle_main"

from bundle_main import checks
print('0 checks - done')

print('prices_updated - initiating. Printing Stock and % Progress.')
from bundle_main import prices_update
print('prices_updated - done')

print('financials_update - initiating. Printing Stock and % Progress.')
from bundle_main import financials_update
print('financials_update - done')

print('financials_update_annually - initiating. Printing Stock and % Progress.')
from bundle_main import financials_update_annually
print('financials_update_annually - done')


print('prices_combine - initiating.')
from bundle_main import prices_process
print('prices_combine - done')

print('financials_process - initiating.')
from bundle_main import financials_process
print('financials_process - done')

print('financials_process_annually - initiating.')
from bundle_main import financials_process_annually
print('financials_process_annually - done')


print('datasets_merge - initiating.')
from bundle_main import datasets_merge
print('datasets_merge - done')

from bundle_main import output
print('output - done')


