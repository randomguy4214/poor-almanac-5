#!/usr/bin/python

import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"


#drop_list = drop_list_industry['Industry'].tolist()
#df = df[~df['Industry'].isin(drop_list)] # drop some industries


# loop through dtypes and divide
for column in df_merged.columns:

    if df_merged[column].dtype != 'object':
        df_merged[column] = df_merged[column].div(1000000)

# reorder and export
cols_to_order = ['Ticker', 'Company Name', 'Industry', 'Fiscal Year']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]

df_merged.to_csv(os.path.join(cwd, input_folder,"3_fundamentals_processed.csv"))

