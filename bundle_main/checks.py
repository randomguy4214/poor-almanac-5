#!/usr/bin/python

import os

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
prices_temp = "prices"
financials_quarterly_temp = "financials_quarterly"
financials_annually_temp = "financials_annually"

# check folder 0_input
if not os.path.exists(os.path.join(cwd,input_folder)):
    os.mkdir(os.path.join(cwd,input_folder))
    print("folder 0_input created")
else:
    print("good! folder 0_input already exists")

# check temp folder
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder)):
    os.mkdir(os.path.join(cwd,input_folder,temp_folder))
    print("temp folder created")
else:
    print("temp folder exists")

# check temp prices folders
if not os.path.exists(os.path.join(cwd,input_folder,temp_folder, prices_temp)):
    os.mkdir(os.path.join(cwd,input_folder,temp_folder, prices_temp))
    print("temp prices csv folder created")
else:
    print("temp prices csv folder exists")

# check prices and financials folders
if not os.path.exists(os.path.join(cwd, input_folder, temp_folder, financials_quarterly_temp)):
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, financials_quarterly_temp))
    print("temp financials csv folder created")
else:
    print("temp financials csv exists")

# check prices and financials folders
if not os.path.exists(os.path.join(cwd, input_folder, temp_folder, financials_annually_temp)):
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, financials_annually_temp))
    print("temp financials_annually folder created")
else:
    print("temp financials_annually exists")

# check drop list tickers
if not os.path.exists(os.path.join(cwd,input_folder,"0_drop_list.xlsx")):
    drop_list = pd.DataFrame({
        'symbol': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        'industry': ['Biotechnology', 0, 0, 0, 0, 0, 0, 0, 0, 0
                    , 'Shell Companies', 'Banks—Regional', 0, 0
                    , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        'country': ['United States', 'Germany', 'France', 'United Kingdom', 'Belgium', 'Netherlands Antilles'
                    , 'South Korea', 'Switzerland', 'Taiwan', 'Austria', 'Netherlands', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                             })

    drop_list.to_excel(os.path.join(cwd,input_folder,"0_drop_list.xlsx"))
    print("drop_list created")
else:
    print("good! drop_list already exists")