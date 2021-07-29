import backtrader 
import datetime
from strategy import TestStrategy

#cerebro connects a data feed w/ the strategy
#cerebro generates a broker by default, with a certain amount of cash

cerebro = backtrader.Cerebro()
cerebro.broker.set_cash(1000000) #set starting cash

data = backtrader.feeds.YahooFinanceCSVData(
    dataname='BTC.csv',
    fromdate=datetime.datetime(2016, 1, 1),
    todate=datetime.datetime(2016, 12, 31),
    reverse=False)

cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(backtrader.sizers.FixedSize, stake=1000)

print('Starting Portfolio Value : %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
