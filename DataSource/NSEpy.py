from datetime import date
from nsepy import get_history
from nsepy import get_history
from nsepy.history import get_price_list
from nsepy import get_index_pe_history  
from nsepy.derivatives import get_expiry_date


sbin = get_history(symbol='SBIN',
                   start=date(2015,1,1),
                   end=date(2020,6,19))
print(sbin.tail())



# Stock options (Similarly for index options, set index = True)
stock_fut = get_history(symbol="SBIN",
                        start=date(2015,1,1),
                        end=date(2015,1,10),
                        futures=True,
                        expiry_date=date(2015,1,29))
print(stock_fut.head())

# NIFTY Next 50 index
nifty_next50 = get_history(symbol="NIFTY NEXT 50",
                            start=date(2015,1,1),
                            end=date(2015,1,10),
                            index=True)
# NIFTY50 Equal wight index (random index from the list)
nifty_eq_wt = get_history(symbol="NIFTY50 EQUAL WEIGHT",
                            start=date(2017,6,1),
                            end=date(2017,6,10),
                            index=True)
#Index futures price history
nifty_fut = get_history(symbol="NIFTY",
                        start=date(2015,1,1),
                        end=date(2015,1,10),
                        index=True,
                        futures=True,
                        expiry_date=date(2015,1,29))
# Index P/E Ratio History
nifty_pe = get_index_pe_history(symbol="NIFTY",
                                start=date(2015,1,1),
                                end=date(2015,1,10))
# Fetching Expiry Dates
expiry = get_expiry_date(year=2015, month=1)

# Use Expiry Dates function with get_history
stock_fut_exp = get_history(symbol="SBIN",
                            start=date(2015,1,1),
                            end=date(2015,1,10),
                            futures=True,
                            expiry_date=get_expiry_date(2015,1))

# Daily Bhav Copy
prices = get_price_list(dt=date(2015,1,1))