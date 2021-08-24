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
output_folder = "0_output"
drop_list_folder = "drop_list"

# import csv with relevant data
df = pd.read_csv(os.path.join(cwd,input_folder,"2_prices_additional_calc.csv"), index_col=0)
df['price'] = df['price'].astype(float)
#print(df)

# filter out irrelevant
df = df.loc[(df['Date'] == max(df['Date']))] # find max date and drop stocks that are not up-to-date
df = df[~df['symbol'].str.contains('-WS|-H|-I')] # filter out warrants

# filter on different parameters
df = df.loc[(df['price'] < 5)] # price tag less than $5
#df = df.loc[(df['from_low'] < 20)] # less than x% increase from lowest point

# export
df_export = df
df_export = df_export.round(2)
#df_export = df_export.sort_values(by=['NAV_per_share_to_price','from_low'],ascending=[False,True], na_position='first')
df_export = df_export.drop_duplicates(subset='symbol', keep="last")
df_export.reset_index(drop=True, inplace=True)
df_export.to_csv(os.path.join(cwd,input_folder,"3_narrowed_filter.csv"))
#print(df_export)

# export tickers
stocks = df_export[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"3_tickers_narrowed.csv"), index = False)