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
financials_temp = "financials"




########## FIX HERE THE LOOP



financials_table = []
# reorder and export
financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table.to_csv(os.path.join(cwd,input_folder,"2_prices_updated.csv"))
financials_table.to_excel(os.path.join(cwd,input_folder,"2_prices_updated.xlsx"))


# export tickers
stocks = financials_table[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"3_tickers_filtered.csv"), index = False)

df_columns=pd.DataFrame(financials_table.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'2_prices_updated_columns.xlsx'))










# import prices
prices_table = pd.read_csv(os.path.join(cwd,input_folder,"2_prices_updated.csv"))
fundamentals_table = pd.read_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed.csv"))


df_latest_price = pd.merge(df_prices_highest_dates, prices_table, how='inner', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_latest_price.drop([col for col in df_latest_price.columns if 'drop' in col], axis=1, inplace=True)
df_latest_price = df_latest_price[['symbol','Date','price']]

# adding from low/high
df_merged['from_low'] = (df_merged['price'] - df_merged['low'])/df_merged.low * 100
df_merged['from_high'] = (df_merged['price'] - df_merged['high'])/df_merged.high * 100

df_merged['from_low'] = df_merged['from_low'].astype(int)
df_merged['from_high'] = df_merged['from_high'].astype(int)

# reorder and export
cols_to_order = ['symbol', 'price', 'low', 'high', 'from_low', 'from_high']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]
df_merged.to_csv(os.path.join(cwd,input_folder,"3_prices_additional_calc.csv"))

# pre-filter stocks for the export
prices_additional_calc = pd.read_csv(os.path.join(cwd,input_folder,"4_prices_additional_calc.csv"),usecols = ['symbol', 'from_low'])
prices_filter = prices_additional_calc[~prices_additional_calc['symbol'].str.contains('-|_')]
prices_filter.reset_index(drop=True)

# export tickers
stocks = prices_filter[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"3_tickers_filtered.csv"), index = False)