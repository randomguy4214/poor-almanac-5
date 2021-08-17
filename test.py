
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





#data = yf.download(tickers_string, start="2020-08-15", end="2021-08-15",
#                   group_by="ticker",  threads = True)
#data.to_csv(os.path.join(cwd,input_folder,"yf_test2.csv"))

