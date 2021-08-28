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

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,input_folder,"1_tickers_narrowed.csv"))
#tickers_narrowed = tickers_narrowed[tickers_narrowed['symbol'].str.contains("DE000A2GSVV5|ALTUW|UROY")] #test tickers
#tickers_narrowed = tickers_narrowed #.head(n=3)  #test tickers
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

index_max = pd.to_numeric(tickers_narrowed.index.values.max())
from yahoo_fin.stock_info import * #initiate yahoo_fin
financials_table = []
company_info = []
for t in tickers.split(' '):
    try:
        # progress number
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        print(t, n/index_max*100)

        # get quote
        df_yf_get_quote_table = get_quote_table(t, dict_result=True)
        df = pd.DataFrame.from_dict(df_yf_get_quote_table, orient='index')
        df = df.T
        df['symbol'] = t

        # append
        financials_table.append(df)

    except:
        pass

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


