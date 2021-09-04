
import pandas as pd
import os
pd.options.mode.chained_assignment = None

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# import
fundamentals_table = pd.read_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed.csv"), low_memory=False)
df = fundamentals_table
df.value_counts(subset=['symbol'], sort=False)


print(df)
