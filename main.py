#!/usr/bin/python

bundle_main = "bundle_main"

from bundle_main import checks

# multithreaded import of fundamentals quarterly and annually.
from threading import Thread
def a():
    from bundle_main import prices_update
    from bundle_main import prices_process
def b():
    from bundle_main import financials_update_quarterly
def c():
    from bundle_main import financials_update_annually
    from bundle_main import financials_process_annually

# initiate multithreading
Thread(target=a).start()
Thread(target=b).start()
Thread(target=c).start()

# wait until they will finish
Thread(target=a).join()
Thread(target=b).join()
Thread(target=c).join()

from bundle_main import financials_process_quarterly
from bundle_main import datasets_merge
from bundle_main import output

