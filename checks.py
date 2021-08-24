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
if not os.path.exists(os.path.join(cwd,input_folder,"0_drop_list.xlsx")):
    drop_list = pd.DataFrame({
        'symbol': ['AGOS', 'WPG', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'industry': ['Biotechnology', 'Gold', 'Oil & Gas E&P', 'Oil & Gas Equipment & Services'
                    , 'Oil & Gas Refining & Marketing', 'Other Industrial Metals & Mining'
                    , 'Other Precious Metals & Mining', 'Silver', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'country': ['China', 'Macau', 'Argentina', 'Chile', 'South Africa', 'Cayman Islands', 'Russia', 'India'
                    , 'Greece', 'Brazil', 'Bermuda', 'Japan', 'Australia', 'Cyprus', 'Denmark', 'Peru', 'Spain'
                    , 'Singapore', 'Turkey', 'Israel', 'Hong Kong', 'Netherlands']
                             })
    drop_list.to_excel(os.path.join(cwd,input_folder,"0_drop_list.xlsx"))
    print("drop_list created")
else:
    print("good! drop_list already exists")