# poor-almanac-5

All I want to know is where I'm going to die, so I'll never go there.

The goal is to compare fundamentals with the current market price. 
It downloads all fundamentals data from Yahoo Finance. (Thanks yahoo_fin for making this possible).
Then the data is combined into a large data set, just like Compustat. Limited by Yahoo to 4 years though.
With this data you can do your own research and analysis. 
My original idea was to search for NAV per share > market price. I also have OwnersEarnings. And quarterly rev growth. 
But its all up to you. 

Designed in PyCharm, but will work anywhere. The code relies on yahoo_fin to get the data and pandas to process it.  

1. Define your tickers list in 0_symbols.
2. Run "main.py" and wait A FEW DAYS (Yahoo blocks too many requests, welcome to the world of free data).
3. Run "main_update_only_prices.py" to update only the market prices and recalculate the output.

In case anybody interested to maintain the repo, feel free to connect on reddit.com/user/randomguy53124/.
