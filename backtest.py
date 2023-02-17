# backtester

import backtrader as bt
import datetime
import yfinance as yf


class SmaCross(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        sma1 = bt.ind.SMA(period=30)
        sma2 = bt.ind.SMA(period=50)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()


cerebro = bt.Cerebro()
df = yf.download('AAPL', start='2019-01-01')
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
cerebro.addstrategy(SmaCross)
# add sizer
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
# set commission
cerebro.broker.setcommission(commission=0.001)
# add analyzers
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual_return')
annual_return = cerebro.run()[0].analyzers.annual_return.get_analysis()

for key, value in annual_return.items():
    print(key, value)


cerebro.plot()
