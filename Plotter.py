import matplotlib.pyplot as plt
import mplfinance as mpl


def plot_graph(ticker, df):

    mc = mpl.make_marketcolors(up='green', down='red', inherit=True)
    s = mpl.make_mpf_style(base_mpl_style='ggplot',
    marketcolors=mc, y_on_right=False, mavcolors=['#1f77b4', '#ff7f0e', '#2ca02c'], gridcolor='#b6b6b6',
    gridstyle='--', figcolor='#eee9e9', edgecolor='#8b8585')

    ap = [mpl.make_addplot(df['Bought'], type='scatter',markersize=200,marker='>', color='#29854f', panel=1),
          mpl.make_addplot(df['Sold'], type='scatter', marker='<', markersize=200, color='#720c06', panel=1),
          mpl.make_addplot(df['ATR'], type='line', panel=0, ylabel='ATR', color='#8774AB', secondary_y=False, ylim=(
              min(df['ATR']), max(df['ATR'])
          )),
          mpl.make_addplot(df['Lower B'], type='line', panel=1, color='#3838ea', alpha=0.50),
          mpl.make_addplot(df['Upper B'], type='line', panel=1, color='#3838ea', alpha=0.50),
          mpl.make_addplot(df['70'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='r', alpha=0.25),
          mpl.make_addplot(df['30'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='g', alpha=0.25),
          mpl.make_addplot(df['RSI'], panel=2, type='line', ylabel='RSI', secondary_y=False, ylim=(0, 100)),
          mpl.make_addplot(df['SMA_20'], panel=1, type='line', alpha=0.5, color='orange'),
          mpl.make_addplot(df['macdline'], type='line', color='purple', panel=3, secondary_y=False),
          mpl.make_addplot(df['signalline'], type ='line', color='orange', panel=3, secondary_y=False),
          mpl.make_addplot(df['hist'], type='bar',panel=3, ylabel='MACD',color='#9c9796'),
          mpl.make_addplot(df['0'],type='line',panel=3,color='k',secondary_y=False,
                           ylim=((min(df['signalline']-1), (max(df['signalline']+0.5))))),
          mpl.make_addplot(df['Chandelier_Exit'],type='scatter',marker='_', panel=1)]
    mpl.plot(df, title=ticker, type='candle', style=s, ylabel='Price'
        , addplot=ap, panel_ratios=(0.7, 2, 0.7, 0.8), figratio=(2, 1),
        figscale=1.1, datetime_format='%m-%Y', tight_layout=True, main_panel=1,
             ylim=(min(df['Adj Close']-2), max(df['Adj Close']+2)),
             fill_between=dict(y1=df['Lower B'].values, y2=df['Upper B'].values, color='#f2ad73', alpha=0.20))
    plt.show()
