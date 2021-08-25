#test file


import pandas as pd
import os
import yahoo_fin as yf

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"

from yahoo_fin.stock_info import * #initiate yahoo_fin

t = 'AAPL'
df_yf_stats = get_stats(t)
df_yf_stats.reset_index(drop=True, inplace=True)
df_yf_stats.set_index('Attribute', inplace=True)
#print(df_yf_stats)
df_stats = df_yf_stats.T
df_stats['symbol'] = t
df_stats.reset_index(drop=True, inplace=True)

print(df_stats)


df_stats.to_excel(os.path.join(cwd,input_folder,"test.xlsx"))