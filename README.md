# poor-almanac-5

combining fundamentals of companies and latest prices into one excel output. 
goal is to compare fundamentals with market 

Designed in PyCharm, but will work anywhere
The code relies on 2 things: stooq and yahoo_fin 
    a. yahoo_fin instead of yfinance or anything else - good luck finding free / opensource api that pulls fundamentals 
    b. similar reason for stooq as an input for prices - yahoo/anything else will block you after a few requests
    c. therefore there is a pre-filter for some stocks to reduce requests to yahoo_fin.
   
1. Download from https://stooq.com/db/h/ for US on a daily level
2. Create folders 0_input and 0_output
3. Extract "data" folder from stooq into 0_input
4. Run "main.py" to loop through all the scripts ~~and you will get 2 files~~ 
~~5. There is a huge filter in "prices_additional_calc" at the end of the code that will significantly impact the speed~~
fix is coming soon.

things to add in the future: 
1. Info from options chains: mainly if there are options and what is the IV on nearest calls. Maybe open interest. 
2. FINRA data to gauge short interest. question is how to find good info with as little latency as possible.  
