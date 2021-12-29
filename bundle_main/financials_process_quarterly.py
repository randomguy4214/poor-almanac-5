#!/usr/bin/python

print('financials_update_annually - initiating. Printing Stock and % Progress.')

import os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

cwd = os.getcwd()
input_folder = "0_input"
temp_folder = "temp"
financials_temp = "financials_quarterly"

from pathlib import Path
paths = Path(os.path.join(cwd,input_folder,temp_folder,financials_temp)).glob('**/*.csv')

financials_table = []
for path in paths:
    path_in_str = str(path)
    try:
        fundamentals_parse = pd.read_csv(path,low_memory=False)
        fundamentals_parse = fundamentals_parse[fundamentals_parse['Most Recent Quarter (mrq)'].str.contains("2020|2021|2022|2023|2024|2025|2026|2027", na=False)]
        if not fundamentals_parse.empty:
            financials_table.append(fundamentals_parse)
            print(path_in_str)
        else:
            pass
    except:
        pass

# export
financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table.to_csv(os.path.join(cwd,input_folder,"4_fundamentals_processed_quarterly.csv"), index=False)
financials_table.to_excel(os.path.join(cwd,input_folder,"4_fundamentals_processed_quarterly.xlsx"))

# export tickers
stocks = financials_table[['symbol']].astype(str).drop_duplicates()
stocks = stocks.sort_values(by=['symbol'], ascending= True)
stocks.to_csv(os.path.join(cwd,input_folder,"4_tickers_filtered_quarterly.csv"), index = False)

# export column
df_columns=pd.DataFrame(financials_table.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'4_fundamentals_columns_quarterly.xlsx'))

print('financials_update_annually - done')