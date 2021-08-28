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

t = 'DE000A2GSVV5'
df_yf_financials = get_financials(t, yearly=False, quarterly=True)

print(df_yf_financials)

#df.to_excel(os.path.join(cwd,input_folder,'0_symbols.xlsx'))
