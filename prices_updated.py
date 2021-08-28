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
prices_folder = "stooq"
output_folder = "0_output"

# find 52weeks
from datetime import date,timedelta
today = int(str(date.today()).replace("-",""))
yearago = int(str(date.today() - timedelta(days=365)).replace("-",""))

ticker = 'DE000A2GSVV5'