# poor-almanac-5

combining fundamentals of companies and latest prices into one excel output. 
goal is to compare fundamentals with market 

1. Designed in PyCharm, but will work anywhere
2. The code relies on 2 things: SimFin+ and stooq
3. Download from https://stooq.com/db/h/ for US on a daily level
4. Create folders 0_input and 0_output
5. Extract "data" folder from stooq into 0_input
6. Run "main.py" to loop through all the scripts and you will get 2 files 
7. There is a huge filter in "prices_additional_calc" at the end of the code that will significantly impact the speed

things to add in the future: 
1. Info from options chains: mainly if there are options and what is the IV on nearest calls. Maybe open interest. 
2. FINRA data to gauge short interest. question is how to find good info with as little latency as possible.  
