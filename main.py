#!/usr/bin/python

bundle_main = "bundle_main"

from bundle_main import checks
print('0 checks - done')

print('prices_updated - initiating. Printing Stock and % Progress.')
from bundle_main import prices_update
print('prices_updated - done')

print('prices_process - initiating.')
from bundle_main import prices_process
print('prices_process - done')

# multithreaded import of fundamentals quarterly and annually.
from threading import Thread
def a():
    print('financials_process_quarterly - initiating.')
    from bundle_main import financials_process_quarterly
    print('financials_process_quarterly - done')
def b():
    print('financials_update_quarterly - initiating. Printing Stock and % Progress.')
    from bundle_main import financials_update_quarterly
    print('financials_update_quarterly - done')

Thread(target=a).start()
Thread(target=b).start()



print('financials_process_annually - initiating.')
from bundle_main import financials_process_annually
print('financials_process_annually - done')

print('financials_update_annually - initiating. Printing Stock and % Progress.')
from bundle_main import financials_update_annually
print('financials_update_annually - done')


print('datasets_merge - initiating.')
from bundle_main import datasets_merge
print('datasets_merge - done')

from bundle_main import output
print('output - done')

