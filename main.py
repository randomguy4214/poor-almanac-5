#!/usr/bin/python

import checks
print('0 checks - done')

print('1 prices_updated - initiating')
import prices_updated
print('1 prices_updated - done')

print('2 prices_additional_calc - initiating')
import prices_additional_calc
print('2 prices_additional_calc - done')

print('3 narrowed_filter - initiating')
import narrowed_filter
print('3 narrowed_filter - done')

print('4 prepare_financials - initiating. Printing Stock and Progress')
import prepare_financials
print('4 prepare_financials - done')

import merge_datasets
print('5 merge_datasets - done')


