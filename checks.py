#!/usr/bin/python

import pandas as pd
import os
import sys
pd.options.mode.chained_assignment = None  # default='warn'

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"

# check folder 0_input
if not os.path.exists(os.path.join(cwd,input_folder)):
    os.mkdir(os.path.join(cwd,input_folder))
    print("folder 0_input created")
else:
    print("good! folder 0_input already exists")

# check folder data
if not os.path.exists(os.path.join(cwd,input_folder,prices_folder)):
    print("bad! you need to download and unzip from https://static.stooq.com/db/h/d_us_txt.zip")
    print("please download first. exiting the code")
    sys.exit()
else:
    print("good! folder data already exists. but are you sure it has the latest info? please go to https://static.stooq.com/db/h/d_us_txt.zip")

# check drop list tickers
if not os.path.exists(os.path.join(cwd,input_folder,"0_drop_list.csv")):
    drop_list = pd.DataFrame({'symbol': ['AGOS'],
                       'industry': ['Biotechnology'],
                       'country': ['China']})
    drop_list.to_csv(os.path.join(cwd,input_folder,"0_drop_list.csv"))
    print("drop_list created")
else:
    print("good! drop_list already exists")