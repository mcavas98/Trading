import pandas as pd


def average_true_range(df, n):

	trlist = []
	for i in range(len(df.index)-1):
		if i == 0:
			trlist.append(0)
		else:
			x = (df.iloc[i]['High'])
			y = (df.iloc[i]['Low'])
			z = (df.iloc[i-1]['Adj Close'])
			x1, x2, x3 = (x-y), abs(x-z), abs(y-z)
			trlist.append(max(x1, x2, x3))
	m = pd.Series(trlist, index=df.index[:-1])
	df['ATR'] = m.ewm(alpha=1/n).mean()
	return df


def relative_strength_index(df, n=14):
	diff = df['Adj Close'].diff(1)

	up_chg = 0 * diff
	down_chg = 0 * diff
	up_chg[diff > 0] = diff[diff > 0]
	down_chg[diff < 0] = diff[diff < 0]
	up_chg_avg = up_chg.ewm(com=n-1, min_periods=n).mean()
	down_chg_avg = down_chg.ewm(com=n-1, min_periods=n).mean()
	rs = abs(up_chg_avg/down_chg_avg)
	rsi = 100 - 100/(1+rs)
	df['RSI'] = rsi
	df['70'] = 70
	df['30'] = 30
	return df


def bollinger_bands(df, mav, k):

	df['SMA_' + str(mav)] = df['Adj Close'].rolling(window=mav, min_periods=1).mean()

	std = pd.Series(df['Adj Close'].rolling(window=mav).std(ddof=0))

	df['Upper B'] = df['SMA_' + str(mav)] + (k*std)
	df['Lower B'] = df['SMA_' + str(mav)] - (k*std)
	return df


def macd(df, n1, n2, n3):
	df["EMA_" + str(n1)] = df["Adj Close"].ewm(span=n1, adjust=False).mean()
	df["EMA_" + str(n2)] = df["Adj Close"].ewm(span=n2, adjust=False).mean()
	df["EMA_" + str(n3)] = df["Adj Close"].ewm(span=n3, adjust=False).mean()

	df['macdline'] = round(df["EMA_" + str(n2)] - df["EMA_" + str(n1)], 2)
	df['signalline'] = round(df['macdline'].ewm(span=n3, adjust=False).mean(), 2)
	df['hist'] = round(df['macdline']-df['signalline'], 2)
	df['0'] = 0
	return df


def chandelier_exit(df,days,multiplier):

	df['Chandelier_High'] = df['High'].rolling(window=days).max()
	df['Chandelier_Exit'] = df['Chandelier_High'] - multiplier*df['ATR']

	return df
