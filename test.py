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

t = 'BIOYF'
df_yf_get_quote_table = get_quote_table(t , dict_result = True)
df = pd.DataFrame.from_dict(df_yf_get_quote_table, orient='index')
df = df.T
df['symbol'] = t


print(df)

df.to_excel(os.path.join(cwd,input_folder,'df.xlsx'))

