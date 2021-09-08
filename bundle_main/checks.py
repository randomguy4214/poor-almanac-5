#!/usr/bin/python

import os

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
prices_temp = "prices"
financials_temp = "financials"
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
if not os.path.exists(os.path.join(cwd, input_folder, temp_folder, financials_temp)):
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, financials_temp))
    print("temp financials csv folder created")
else:
    print("temp financials csv exists")

# check prices and financials folders
if not os.path.exists(os.path.join(cwd, input_folder, temp_folder, financials_temp)):
    os.mkdir(os.path.join(cwd, input_folder, temp_folder, financials_annually_temp))
    print("temp financials_annually folder created")
else:
    print("temp financials_annually exists")

# check drop list tickers
if not os.path.exists(os.path.join(cwd,input_folder,"0_drop_list.xlsx")):
    drop_list = pd.DataFrame({
        'symbol': ['AGOS', 'WPG', 'GME', 'NVCN', 'INPX', 'BRH.DE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        'industry': ['Biotechnology', 'Gold', 'Oil & Gas E&P', 'Oil & Gas Equipment & Services'
                    , 'Oil & Gas Refining & Marketing', 'Other Industrial Metals & Mining'
                    , 'Other Precious Metals & Mining', 'Silver', 'Asset Management', 'Insurance—Property & Casualty'
                    , 'Shell Companies', 'Banks—Regional', 'Insurance—Life', 'Banks—Diversified'
                    , 'Mortgage Finance', 'REIT—Mortgage', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        'country': ['China', 'Macau', 'Argentina', 'Chile', 'South Africa', 'Cayman Islands', 'Russia', 'India'
                    , 'Greece', 'Brazil', 'Bermuda', 'Japan', 'Australia', 'Cyprus', 'Denmark', 'Peru', 'Spain'
                    , 'Singapore', 'Turkey', 'Israel', 'Hong Kong', 'Netherlands', 'Philippines', 'Romania', 'Mexico', 'New Zealand', 'Canada'
                    , 'Indonesia', 'Malaysia', 'Thailand', 'Mongolia', 'Norway', 'Sweden', 'Isle of Man'
                    , 'Italy', 'Finland']
                             })
    drop_list.to_excel(os.path.join(cwd,input_folder,"0_drop_list.xlsx"))
    print("drop_list created")
else:
    print("good! drop_list already exists")