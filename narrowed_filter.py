#!/usr/bin/python

import pandas as pd
import os

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
output_folder = "0_output"

# import file with relevant data
df_input = pd.read_excel(os.path.join(cwd,input_folder,"0_symbols.xlsx"), sheet_name='Sheet1', header=0)
df = df_input.dropna(subset=['symbol']).astype('str')

# filter out irrelevant
df = df[~df['symbol'].str.contains('-WS|-H|-I|-B|-U|_B')] # filter out unnecessary

# export
df_export = df
df_export = df_export.drop_duplicates(subset='symbol', keep="last")
df_export.reset_index(drop=True, inplace=True)

# export tickers
stocks = df_export['symbol'].sort_values(ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"1_tickers_narrowed.csv"), index = False)