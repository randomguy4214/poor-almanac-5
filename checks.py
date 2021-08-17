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
    print("bad! you need to donwload and unzip from https://static.stooq.com/db/h/d_us_txt.zip")
    print("please download first. exiting the code")
    sys.exit()
else:
    print("good! folder data already exists. but are you sure it has the latest info? please go to ")

# check drop list tickers
if not os.path.exists(os.path.join(cwd,input_folder,"0_drop_list_ticker.csv")):
    drop_list_ticker_dict = {'symbol': ['AGOS']}
    drop_list_ticker = pd.DataFrame(data=drop_list_ticker_dict)
    drop_list_ticker.to_csv(os.path.join(cwd,input_folder,"0_drop_list_ticker.csv"))
    print("drop_list_ticker created")
else:
    print("good! drop_list_ticker already exists")

# check drop list industries
if not os.path.exists(os.path.join(cwd,input_folder,"0_drop_list_industry.csv")):
    drop_list_industry_dict = {'Industry': ['Biotechnology']}
    drop_list_industry = pd.DataFrame(data=drop_list_industry_dict)
    drop_list_industry.to_csv(os.path.join(cwd,input_folder,"0_drop_list_industry.csv"))
    print("drop_list_industry created")
else:
    print("good! drop_list_industry already exists")