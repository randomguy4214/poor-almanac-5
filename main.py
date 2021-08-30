#!/usr/bin/python

import checks
print('0 checks - done')

print('prices_updated - initiating')
import prices_update
print('prices_updated - done')

print('prices_additional_calc - initiating')
import prices_combine
print('prices_additional_calc - done')

print('prepare_financials - initiating. Printing Stock and Progress')
import financials_update
print('prepare_financials - done')

print('financials_combine - initiating.')
import financials_combine
print('financials_combine - done')

print('datasets_merge - initiating.')
import datasets_merge
print('datasets_merge - done')

import output
print('output - done')


