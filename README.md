# poor-almanac-5

combining fundamentals of companies and latest prices into one excel output. 
goal is to compare fundamentals with the market.

Designed in PyCharm, but will work anywhere. The code relies on 2 things to get the financial data: stooq and yahoo_fin. 
And pandas to process the data.  

1. Download from https://static.stooq.com/db/h/d_us_txt.zip
2. Run "main.py" to loop through all the scripts
3. If error, extract "data" folder from stooq into "stooq" folder
4. Find the file with the highest numeration to see the processed results in a neat view. everything in between is for checks / curiosity.

things to add in the future: 
1. European stocks
2. Info from options chains: mainly if there are options and what is the IV on nearest calls. Maybe open interest. 
3. FINRA data to gauge short interest. question is how to find good info with as little latency as possible.  
