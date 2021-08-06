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

# import csv with relevant data
df = pd.read_csv(os.path.join(cwd,input_folder,"4_fundamentals_last_quarter.csv"))
df['price'] = df['price'].astype(float)

# export as full to xlsx for debugging purposes
df.to_excel(os.path.join(cwd,output_folder,"4_df_export.xlsx"),sheet_name='output', index=False)

# filter on logic
df = df.loc[(df['price'] < 5)] # price tag less than $5
df = df.loc[(df['from_low'] < 15)] # less than x% increase from lowest point
df = df.loc[(df['NAV_per_share_to_price'] > 0.5)] # Book to market is less than x%

# filter on tickets
drop_list = pd.read_csv(os.path.join(cwd,input_folder,"drop_list.csv"))
drop_list = drop_list['symbol'].tolist()
df = df[~df['symbol'].isin(drop_list)] # drop some tickers

df_export = df
# df_export = df.query('NAV_to_price > 0')
df_export = df_export.round(2)
df_export = df_export.sort_values(by=['NAV_per_share_to_price','from_low'],ascending=[False,True], na_position='first')
df_export = df_export.drop_duplicates(subset='symbol', keep="last")
df_export.to_excel(os.path.join(cwd,output_folder,"5_df_export.xlsx"),sheet_name='output', index=False)
#print(df_export)