#!/usr/bin/python

import pandas as pd
import os

# formatting
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"

# find 52weeks
from datetime import date,timedelta
today = int(str(date.today()).replace("-",""))
yearago = int(str(date.today() - timedelta(days=365)).replace("-",""))

from pathlib import Path
paths = Path(os.path.join(cwd,input_folder,prices_folder)).glob('**/*.txt')

prices_table = []
for path in paths:
    path_in_str = str(path)
    try:
        if ('etfs|-|_') not in path_in_str: # loop through folders and filter out weird shit
            tickers_parse = pd.read_csv(path,low_memory=False)
            tickers_parse['<DATE>'] = tickers_parse['<DATE>'].astype(int)
            tickers_parse = tickers_parse[tickers_parse['<DATE>'] > yearago]
            tickers_parse['symbol'] = tickers_parse['<TICKER>'].str.replace(".US","",regex=True)
            #,<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>
            prices_table.append(tickers_parse)
    except:
        pass

prices_table = pd.concat(prices_table)
prices_table.drop_duplicates()
prices_table.columns = ['symbol_dot', 'per', 'Date', 'time', 'open', 'high', 'low', 'price', 'vol', 'openint', 'symbol']
prices_table.to_csv(os.path.join(cwd,input_folder,"1_prices_updated.csv"))



