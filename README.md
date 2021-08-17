# poor-almanac-5

combining fundamentals of companies and latest prices into one excel output. 
goal is to compare fundamentals with the market.

Designed in PyCharm, but will work anywhere. The code relies on 2 things: stooq and yahoo_fin 

    good luck finding free / opensource api that pulls fundamentals 
    yahoo_fin instead of yfinance or anything else
    similar reason for stooq as an input for prices - yahoo/anything else will block you after a few requests
    therefore there is a pre-filter for some stocks to reduce requests to yahoo_fin.
   
1. Download from https://static.stooq.com/db/h/d_us_txt.zip
2. Run "main.py" to loop through all the scripts
3. If error, extract "data" folder from stooq into 0_input
4. "narrowed filter" reduces the number of stocks universe to apply yahoo_fin for.

  `# filter on different parameters`

   `df = df.loc[(df['price'] < 5)] # price tag less than $5`

   `df = df.loc[(df['from_low'] < 15)] # less than 15% increase from the lowest point`

5. Check file with the highest numeration to see the processed results in a neat view. everything in between is for checks / curiosity.

things to add in the future: 
1. Info from options chains: mainly if there are options and what is the IV on nearest calls. Maybe open interest. 
2. FINRA data to gauge short interest. question is how to find good info with as little latency as possible.  
