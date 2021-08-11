#!/usr/bin/python

import pandas as pd
import os
import investpy
pd.options.mode.chained_assignment = None  # default='warn'

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

# import prices
prices_table = pd.read_csv(os.path.join(cwd,input_folder,"1_prices_updated.csv"))
#test = prices_table[(prices_table == 'HRL').any(axis=1)] #debug
#test.to_csv(os.path.join(cwd,input_folder,"test.csv"), index = False)

# extract current price
df_prices_highest_dates = prices_table[['symbol','Date']]
df_prices_highest_dates['Date'] = df_prices_highest_dates['Date'].astype(int)
df_prices_highest_dates = df_prices_highest_dates.groupby(['symbol'])
df_prices_highest_dates = df_prices_highest_dates.max()

df_latest_price = pd.merge(df_prices_highest_dates, prices_table, how='inner', left_on=['symbol', 'Date'], right_on=['symbol', 'Date'], suffixes=('', '_drop'))
df_latest_price.drop([col for col in df_latest_price.columns if 'drop' in col], axis=1, inplace=True)
df_latest_price = df_latest_price[['symbol','Date','price']]
#print(df_latest_price[(df_latest_price == 'HRL').any(axis=1)]) #debug

# importing prices to find highest / lowest for 52week
df_prices = prices_table
df_prices_min = df_prices.groupby(['symbol'])['low'].min()
df_prices_max = df_prices.groupby(['symbol'])['high'].max()

# latest price, high, low, etc
df_merged = pd.merge(df_latest_price, df_prices_min, how='inner', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged = pd.merge(df_merged, df_prices_max, how='inner', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged = df_merged.drop_duplicates(subset='symbol',keep='first')

# adding from low/high
df_merged['from_low'] = (df_merged['price'] - df_merged['low'])/df_merged.low * 100
df_merged['from_high'] = (df_merged['price'] - df_merged['high'])/df_merged.high * 100

df_merged['from_low'] = df_merged['from_low'].astype(int)
df_merged['from_high'] = df_merged['from_high'].astype(int)

# reorder and export
cols_to_order = ['symbol', 'price', 'low', 'high', 'from_low', 'from_high']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]
df_merged.to_csv(os.path.join(cwd,input_folder,"2_prices_additional_calc.csv"))

# pre-filter stocks for the export
prices_additional_calc = pd.read_csv(os.path.join(cwd,input_folder,"2_prices_additional_calc.csv"),usecols = ['symbol', 'from_low'])
prices_filter = prices_additional_calc[~prices_additional_calc['symbol'].str.contains('-|_')]
prices_filter.reset_index(drop=True)

# export tickers
stocks = prices_filter[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"2_tickers_filtered.csv"), index = False)