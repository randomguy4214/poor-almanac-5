# poor-almanac-5

combining fundamentals of companies and latest prices into one excel output. 
goal is to compare fundamentals with the market.

Designed in PyCharm, but will work anywhere. The code relies on yahoo_fin to get the data and pandas to process it.  

1. Run "main.py" to loop through all the scripts
2. It runs incredibly slow (few days prob), because yahoo is blocking too many requests. And the code aims to get as much as possible.
3. You need to manually "delete temp folder" when you want to update everything
4. To update only the market prices - run "main_update_only_prices". it will override prices in temp. and will take tickers from 5_tickers_narrowed.csv.

5. Yes, there are files which will be generated, but you cannot see them on github. Because there are limits on uploads size. 
6. Yes, if you know shit about coding it will be a bit of a challenge to install PyCharm and clone the repo. But I did it. So can you.
