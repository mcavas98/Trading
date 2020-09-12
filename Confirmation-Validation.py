import yfinance as yf
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
from datetime import timedelta


#yf.pdr_override()
#startyear = 2018
#startmonth = 1
#startday = 1
#stock = input('Enter ticker: ')
#start = dt.datetime(startyear, startmonth, startday)
#end = dt.datetime(2020, 1, 18)
#now = dt.datetime.now()

#df = pdr.get_data_yahoo(stock, start, end)
df = pd.read_csv("ARCLK.IS.csv")
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df[df['Volume'] > 0]
df.set_index(['Date'], inplace=True)
ma = 5
df['SMA_'+ str(ma)] = df['Adj Close'].rolling(window=ma,min_periods=1).mean()
df = df[ma:]
#df.set_index(['Date'], inplace=True)
pos = 0
num = 0
percentchange = []
print(df.head())
for i in df.index:
    open = df['Open'][i]

    sma = df['SMA_'+ str(ma)][i]

    if open > sma:
        if pos == 0:
            bp = df['Adj Close'][i]
            pos = 1
            print('Buying stock at ' + str(bp))
    elif open < sma:
        if pos == 1:
            sp = df['Adj Close'][i]
            pos = 0
            print('Selling stock at ' + str(sp))
            pc = (sp/bp-1)*100
            percentchange.append(pc)
    if (num == df["Adj Close"].count()-1) & (pos == 1):
        pos = 0
        sp = df['Adj Close'][i]
        print("Selling now at " +str(sp))
        pc = (sp/bp-1)*100
        percentchange.append(pc)

    num += 1

print(percentchange)


gains = 0
ng = 0
losses = 0
nl = 0
totalR = 1

for i in percentchange:
    if(i>0):
        gains += i
        ng += 1
    else:
        losses += i
        nl += 1
    totalR = totalR*((i/100)+1)

totalR = round((totalR-1)*100, 2)

if ng > 0:
    avgGain = gains/ng
    maxR = str(max(percentchange))
else:
    avgGain=0
    maxR = "undefined"


if nl > 0:
    avgLoss = losses/nl
    maxL = str(min(percentchange))
    ratio = str(-avgGain/avgLoss)
else:
    avgLoss = 0
    maxL = "undefined"

if (ng>0 or nl>0):
    battingAvg = ng/(ng+nl)
else:
    battingAvg = 0

print()
print("Results for "+ 'Aselsan Elektronik Sanayi ve Ticaret Anonim Sirketi'  +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades")
print("EMAs used: "+str(ma))
print("Batting Avg: "+ str(battingAvg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avgGain))
print("Average Loss: "+ str(avgLoss))
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )

print()

