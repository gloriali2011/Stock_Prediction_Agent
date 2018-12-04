# Uncomment below line to install alpha_vantage
#!pip install alpha_vantage
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import json
import matplotlib.pyplot as plt
import re

#include the different ways that algorithms can use different technical indicators
#put these technical indicators into use
#
ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
ti = TechIndicators(key='EJ69MPM068NGTJ30', output_format='pandas')

data, meta_data = ts.get_intraday(symbol='EBAY',interval='1min', outputsize='full')

sma_data, sma_meta_data =ti.get_sma(symbol='EBAY',interval='1min', time_period=200, series_type='close')

PRICE_TYPE = '4. close'

#get format the same with other dicts
for index1, row1 in data[PRICE_TYPE].iteritems() :
    new_index = re.sub(':00$', '', index1)
    data[PRICE_TYPE][new_index] = data[PRICE_TYPE].pop(index1)

initial_money = 50000
money = initial_money
shares = 0
avg_greater_than_data_previous = False

for index, row in sma_data.iteritems() :
    for time, avg_price in row.iteritems():
        print time
        if time in data[PRICE_TYPE]:
            real_price = data[PRICE_TYPE][time]
            if real_price > avg_price:
                if avg_greater_than_data_previous:
                    if money > 20 * real_price:
                        print "buy"
                        shares += 20
                        money -= 20*real_price
                    avg_greater_than_data_previous = False
                else:
                    print "hold"
            else:
                if not avg_greater_than_data_previous:
                    if shares > 20:
                        print "sell"
                        shares -= 20
                        money += 20 * real_price
                    avg_greater_than_data_previous = True
                else:
                    print "hold"



print "You initially had $", initial_money
print "You have $",money," left"
print "You are holding ",shares," shares"
print "The current price for your stock is: $",real_price
print "The value of your shares is: $",shares * real_price
print "Your profit is: $", shares * real_price + money - initial_money

#data[PRICE_TYPE].plot()
#sma_data.plot()
#plt.title('SMA indicator for  MSFT stock (1 day)')
#plt.show()

#print(data.head(100))


