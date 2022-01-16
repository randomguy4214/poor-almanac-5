#!/usr/bin/python

print('prices_update - initiating.')

import os
import pandas as pd
from datetime import date

# formatting
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

#check year
todays_date = date.today()
curr_year = todays_date.year

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

# find last updated ticker (this is necessary if you lose internet connection, etc)
prices_last_ticker = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"),index_col=0)
last_ticker_n = prices_last_ticker.values[0]
last_ticker_nn = last_ticker_n[0]
print("last ticker in prices update was number ", last_ticker_nn)

# start importing the prices
index_max = pd.to_numeric(tickers_narrowed.index.values.max())
from yahoo_fin.stock_info import * #initiate yahoo_fin
company_info = []

for t in tickers.split(' '):
    try:
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        if n > last_ticker_nn:
            # check if last quarter is recent (many tickers are dead for example)
            df_yf_stats = get_stats(t)
            df_check_mrq = df_yf_stats["Value"][df_yf_stats["Attribute"] == "Most Recent Quarter (mrq)"]
            datetime_object = pd.to_datetime(df_check_mrq)  # , errors='coerce')
            df_mrq_year = datetime_object.dt.year
            mrq_year = df_mrq_year.values[0]

            if (mrq_year + 1) >= curr_year:
                name = t + ".csv"
                # get quote
                df_yf_get_quote_table = get_quote_table(t, dict_result=True)
                df = pd.DataFrame.from_dict(df_yf_get_quote_table, orient='index')
                df = df.T
                df['symbol'] = t
                # export
                df.to_csv(os.path.join(cwd, input_folder, temp_folder, prices_temp, name), index=False)
                # print & export last_n
                nn = n[0] # get number out of numpy.array
                nnn = round(nn/index_max*100,2)
                print(t, "/", nnn, "% /", nn, "from", index_max, "/ prices")
                prices_last_ticker = pd.DataFrame({'number':n})
                prices_last_ticker.to_csv(os.path.join(cwd, input_folder, temp_folder, "prices_last_ticker.csv"))

    except:
        pass

prices_last_ticker = pd.DataFrame({'number': [0] })
prices_last_ticker.to_csv(os.path.join(cwd,input_folder,temp_folder,"prices_last_ticker.csv"))

print('prices_update - done')
