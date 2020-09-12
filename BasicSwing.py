import pandas as pd
import numpy as np
from Plotter import plot_graph
from Technical_Indicators import average_true_range
from Technical_Indicators import relative_strength_index
from Technical_Indicators import bollinger_bands
from Technical_Indicators import macd,chandelier_exit
ticker = 'ECZYT.IS'
df = pd.read_csv('../stockdata/'+ticker+'.csv')

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df[df['Volume'] > 0]
df.set_index(['Date'], inplace=True)

emas = [9, 13, 50]
for i in range(len(emas)):
	df["EMA_" + str(emas[i])] = round(df["Adj Close"].ewm(span=emas[i], adjust=False).mean(), 2)


pos, num, percentchange = 0, 0, []
buys_scatter = pd.Series(np.nan, index=df.index)
sells_scatter = pd.Series(np.nan, index=df.index)

relative_strength_index(df, 14), average_true_range(df, 14), bollinger_bands(df, 20, 2)
macd(df, 26, 12, 9), chandelier_exit(df, 22, 3)

for i in range(len(df.index)):
	fifty = df['EMA_50'][i]
	thirteen = df['EMA_13'][i]
	nine = df['EMA_9'][i]
	close = df['Adj Close'][i]
	n_close = df['Close'][i]
	atr = df['ATR'][i]
	prev = df['Adj Close'][i-1]
	rsi = df['RSI'][i]
	prev_rsi = df['RSI'][i-1]
	chan_exit = df['Chandelier_Exit'][i]
	open = df['Open'][i]
	signalline, prev_signalline = df['signalline'][i], df['signalline'][i-1]
	macdline, prev_macdline = df['macdline'][i], df['macdline'][i-1]
	upperb, lowerb = df['Upper B'][i], df['Lower B'][i]
	if pos == 0:
		if (nine >= thirteen) & (thirteen > fifty) & ((close > thirteen) & (close > nine) & (close > fifty)):
			pos = 1
			bp = close
			print('Buying now at ' + str(bp),'1')
			buys_scatter[i] = close
		elif (signalline < 0) and (macdline < 0):
			if (prev_macdline < prev_signalline) & (macdline > signalline):
				pos = 1
				bp = close
				print('Buying now at ' + str(bp),'2')
				buys_scatter[i] = close
		elif (n_close < lowerb) & (i > 0):
				print('lower b', df.index[i])
				pos = 1
				bp = close
				print('Buying now at ' + str(bp),'3')
				buys_scatter[i] = close
	elif pos == 1:
		
		if (signalline > 0) and (macdline > 0):
			if (prev_macdline > prev_signalline) & (macdline < signalline):
				pos = 0
				sp = close
				print("Selling now at " + str(sp), '1')
				pc = (sp/bp-1)*100
				percentchange.append(pc)
				sells_scatter[i] = close
		elif (close < chan_exit) & ((macdline < 0) & (macdline < signalline)):
			pos = 0
			sp = close
			print("Selling now at " + str(sp), '2')
			pc = (sp/bp-1)*100
			percentchange.append(pc)
			sells_scatter[i] = close
		elif n_close > upperb:
			pos = 0
			sp = close
			print("Selling now at " + str(sp),'3')
			pc = (sp/bp-1)*100
			percentchange.append(pc)
			sells_scatter[i] = close


	if (num == df["Adj Close"].count()-1) & (pos == 1):
		pos = 0
		sp = close
		print("Selling now at " + str(sp))
		pc = (sp/bp-1)*100
		percentchange.append(pc)
		sells_scatter[i] = close
	num += 1
df['Bought'] = buys_scatter
df['Sold'] = sells_scatter

print(percentchange)

gains = 0
number_of_gains = 0
losses = 0
number_of_losses = 0
totalR = 1

for i in percentchange:
    if(i > 0):
        gains += i
        number_of_gains += 1
    else:
        losses += i
        number_of_losses += 1
    totalR = totalR*((i/100)+1)

totalR = round((totalR-1)*100, 2)

if number_of_gains> 0:
    avgGain = gains/number_of_gains
    maxR = str(max(percentchange))
else:
    avgGain = 0
    maxR = "undefined"


if number_of_losses > 0:
	avgLoss = losses/number_of_losses
	maxL = str(min(percentchange))
	ratio = str(-avgGain/avgLoss)
elif (number_of_losses == 0) & (number_of_gains >0):
	print('No losses, ' + str(number_of_gains)+' gains occured')
	avgLoss = 0
	maxL = 0
else:
	avgLoss = 0
	maxL = "undefined"

if number_of_gains > 0 or number_of_losses > 0:
	battingAvg = number_of_gains/(number_of_gains+number_of_losses)
else:
	battingAvg = 0

print()
print(
	"Results for " + ticker + " going back to " + str(df.index[0]) +
	", Sample size: " + str(number_of_gains+number_of_losses) + " trades"
)
print("Batting Avg: " + str(battingAvg))
if number_of_losses > 0:
	print("Gain/loss ratio: " + ratio)
print("Average Gain: " + str(avgGain))
print("Average Loss: " + str(avgLoss))
print("Max Return: " + str(maxR))
print("Max Loss: " + str(maxL))
print("Total return over "+str(number_of_gains+number_of_losses) + " trades: " + str(totalR)+"%")

print()

plot_graph(ticker, df)

print()
#print(df.loc['2020-02-03':'2020-02-10'][['Adj Close','Close','Upper B']])

