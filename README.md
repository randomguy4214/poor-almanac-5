moved to: https://github.com/randomguy4214/poor-almanac-8
this one is just a legacy running on yahoo_fin

# poor-almanac-5

All I want to know is where I'm going to die, so I'll never go there.

The goal is to compare fundamentals with the current market price. 
It downloads all fundamentals data from Yahoo Finance. (Thanks yahoo_fin for making this possible).
Then the data is combined into a large data set, just like Compustat. Limited by Yahoo to 4 years though.
With the data you can do your own research and analysis. 
My original idea was to search for NAV per share > market price. I also have OwnersEarnings. And quarterly rev growth. 
But its all up to you. 

The code relies on yahoo_fin to get the data and pandas to process it.
1. Define your tickers list in 0_symbols.
2. Run "main.py" and wait A FEW DAYS (Yahoo blocks too many requests, welcome to the world of free data).
3. Run "main_update_only_prices.py" to update only the market prices and recalculate the output.

The code consists of 4 main elements that are split into many .py scripts in "bundle_main".
First part is about loading prices and fundamentals (ttm quarters and last 4 years).
In this part, prefiltering is done by checking whether last data is from a year ago or newer. Everything else is not downloaded.
Next part is combining 3 datasets from CSVs on ticker level in "*process* .py" files.
After that, the main dataset is created through "datasets_merge.py".
The last step is in file "output.py" - whatever variables and filters you wish to see, or sorting -> all goes into output files.

In case anybody interested to maintain the repo, feel free to connect on reddit.com/user/randomguy53124/.
