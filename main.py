#!/usr/bin/python

import checks
print('0 checks - done')

print('prices_updated - initiating. Printing Stock and % Progress.')
import prices_update
print('prices_updated - done')

print('prices_combine - initiating.')
import prices_process
print('prices_combine - done')

print('financials_update - initiating. Printing Stock and % Progress.')
import financials_update
print('financials_update - done')

print('financials_combine - initiating.')
import financials_process
print('financials_combine - done')

print('datasets_merge - initiating.')
import datasets_merge
print('datasets_merge - done')

import output
print('output - done')


