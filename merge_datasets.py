#!/usr/bin/python

import pandas as pd
import os
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

# import CSVs
df_prices = pd.read_csv(os.path.join(cwd,input_folder,"2_prices_additional_calc.csv"), index_col=0)
df_fundamentals_processed = pd.read_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed.csv"), index_col=0)

# merge data sets
df_merged = pd.merge(df_fundamentals_processed, df_prices, how='left', left_on=['stock'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.drop_duplicates()
df_merged.reset_index(inplace=True)

# calculate additional variables
df_merged['NAV'] = df_merged['Total Assets'] - df_merged['Total Liabilities']
df_merged['NAV_per_share'] = df_merged['NAV'] / df_merged['sharesOutstanding']
df_merged['NAV_per_share_to_price'] = df_merged.NAV_per_share / df_merged['price']
df_merged['FCF_per_share'] = (df_merged['Cash From Operating Activities'] - df_merged['Cash From Investing Activities']) / df_merged['sharesOutstanding']
df_merged['marg'] = df_merged['Gross Profit'] / df_merged['Total Revenue'] * 100

# reorder
cols_to_order = ['Date','symbol', 'price', 'low', 'high', 'from_low', 'from_high', 'NAV_per_share_to_price', 'FCF_per_share', 'marg']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]
df_merged = df_merged.round(2)
del df_merged['stock']

# export full fundamentals
df_merged.to_csv(os.path.join(cwd,input_folder,'4_fundamentals.csv'), index=False)

# export last period
df_merged.sort_values('Date', ascending=False)
df_merged.drop_duplicates(subset=['symbol'], keep='first', inplace=True)
df_merged.to_csv(os.path.join(cwd,input_folder,'4_fundamentals_last_quarter.csv'), index=False)




