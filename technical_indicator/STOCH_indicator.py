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

stoch_data, stoch_meta_data =ti.get_stoch(symbol='EBAY',interval='1min')

PRICE_TYPE = '4. close'

stoch_slowk = dict()
stoch_slowd = dict()

#get format the same with other dicts
for index1, row1 in data[PRICE_TYPE].iteritems() :
    new_index = re.sub(':00$', '', index1)
    data[PRICE_TYPE][new_index] = data[PRICE_TYPE].pop(index1)

for index, row in stoch_data.iteritems() :
    for time, val in row.iteritems() :
        if time not in stoch_slowk:
            stoch_slowk[time] = val
        else:
            stoch_slowd[time] = val

initial_money = 50000
money = initial_money
shares = 0
slowd_previously_larger_than_slowk = False
real_price = 0

timelist = stoch_slowk.keys()
timelist.sort()
for time in timelist:
    if time in stoch_slowd and time in stoch_slowk:
        print time
        real_price = data[PRICE_TYPE][time]
        if (stoch_slowd[time] > stoch_slowk[time] and not slowd_previously_larger_than_slowk and stoch_slowd[time] > 80):
            if shares > 20:
                print "sell"
                shares -= 20
                money += 20 * real_price
            else:
                print "hold"

        elif (stoch_slowd[time] < stoch_slowk[time] and slowd_previously_larger_than_slowk and stoch_slowd[time] < 20):
            if money > 20 * real_price:
                print "buy"
                shares += 20
                money -= 20 * real_price
            else:
                print "hold"

        else:
            print "hold"

        if stoch_slowd[time] > stoch_slowk[time]:
            slowd_previously_larger_than_slowk = True
        else:
            slowd_previously_larger_than_slowk = False

print "You initially had $", initial_money
print "You have $",money," left"
print "You are holding ",shares," shares"
print "The current price for your stock is: $",real_price
print "The value of your shares is: $",shares * real_price
print "Your profit is: $", shares * real_price + money - initial_money

data[PRICE_TYPE].plot()
# stoch_data.plot()
# plt.title('STOCH indicator for  APPL stock (1 day)')
# plt.show()

#print(data.head(100))



