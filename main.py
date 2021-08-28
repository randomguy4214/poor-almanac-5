#!/usr/bin/python

import checks
print('0 checks - done')

print('narrowed_filter - initiating')
import narrowed_filter
print('narrowed_filter - done')

print('prices_updated - initiating')
import prices_updated
print('prices_updated - done')

print('prepare_financials - initiating. Printing Stock and Progress')
import prepare_financials
print('prepare_financials - done')

print('prices_additional_calc - initiating')
import prices_additional_calc
print('prices_additional_calc - done')

import merge_datasets
print('5 merge_datasets - done')
print('please check which Short % of float is used (line 43)')


