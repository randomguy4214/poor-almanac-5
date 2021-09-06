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

#!/usr/bin/python

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
temp_folder = "temp"
prices_temp = "prices"
financials_temp = "financials"

# import tickers file
#df_input = pd.read_excel(os.path.join(cwd,input_folder,"0_symbols.xlsx"), sheet_name='Sheet1', header=0)
#df = df_input.dropna(subset=['symbol']).astype('str')

# filter out irrelevant
#df = df[~df['symbol'].str.contains('-WS|-H|-I|-B|-U|_B')] # filter out unnecessary

# export
#df_export = df
#df_export = df_export.drop_duplicates(subset='symbol', keep="last")
#df_export.reset_index(drop=True, inplace=True)

# export tickers
#stocks = df_export['symbol'].sort_values(ascending= True).drop_duplicates()
#stocks.to_csv(os.path.join(cwd,input_folder,"1_tickers_narrowed.csv"), index = False)

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,input_folder,"1_tickers_narrowed.csv"))
#tickers_narrowed = tickers_narrowed[tickers_narrowed['symbol'].str.contains("DE000A2GSVV5|ALTUW|UROY")] #test tickers
#tickers_narrowed = tickers_narrowed #.head(n=3)  #test tickers
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

index_max = pd.to_numeric(tickers_narrowed.index.values.max())
from yahoo_fin.stock_info import * #initiate yahoo_fin
company_info = []
for t in tickers.split(' '):
    try:
        # progress number
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        print(t, n/index_max*100)

        name = t + ".csv"
        if not os.path.exists(os.path.join(cwd, input_folder, temp_folder, prices_temp, name)):
            # get quote
            df_yf_get_quote_table = get_quote_table(t, dict_result=True)
            df = pd.DataFrame.from_dict(df_yf_get_quote_table, orient='index')
            df = df.T
            df['symbol'] = t
            # export
            df.to_csv(os.path.join(cwd, input_folder, temp_folder, prices_temp, name), index=False)
        else:
            pass
    except:
        pass



