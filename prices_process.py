#!/usr/bin/python

import pandas as pd
import os
pd.options.mode.chained_assignment = None

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
prices_temp = "prices"

from pathlib import Path
paths = Path(os.path.join(cwd,input_folder,temp_folder,prices_temp)).glob('**/*.csv')

prices_table = []
for path in paths:
    path_in_str = str(path)
    try:
        tickers_parse = pd.read_csv(path,low_memory=False)
        prices_table.append(tickers_parse)
        print(path_in_str)
    except:
        pass

# reorder and export
prices_table = pd.concat(prices_table)
prices_table.drop_duplicates()
prices_table.to_csv(os.path.join(cwd,input_folder,"2_prices_updated.csv"), index=False)
prices_table.to_excel(os.path.join(cwd,input_folder,"2_prices_updated.xlsx"))

# export tickers
stocks = prices_table[['symbol']].astype(str).sort_values(by=['symbol'], ascending= True)
stocks.drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"2_tickers_filtered.csv"), index = False)

df_columns=pd.DataFrame(prices_table.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'2_prices_updated_columns.xlsx'))
