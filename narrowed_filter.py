#!/usr/bin/python

import pandas as pd
import os

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"
drop_list_folder = "drop_list"

# import csv with relevant data
df = pd.read_csv(os.path.join(cwd,input_folder,"2_prices_additional_calc.csv"), index_col=0)
df['price'] = df['price'].astype(float)

# filter out irrelevant
df = df.loc[(df['Date'] == max(df['Date']))] # find max date and drop stocks that are not up-to-date
df = df[~df['symbol'].str.contains('-WS|-H|-I|-B|-U|_B')] # filter out unnecessary

# export
df_export = df
df_export = df_export.round(2)
df_export = df_export.drop_duplicates(subset='symbol', keep="last")
df_export.reset_index(drop=True, inplace=True)
df_export.to_csv(os.path.join(cwd,input_folder,"3_narrowed_filter.csv"))
#print(df_export)

# export tickers
stocks = df_export[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"3_tickers_narrowed.csv"), index = False)