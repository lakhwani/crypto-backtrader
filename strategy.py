import backtrader

#Compares current day and must be less than prev day
#Compares prev day with its previous day and if prev < prevprev
#-> buy considering buying dip and checking if profit long-term

class TestStrategy(backtrader.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        #official order not made yet
        if order.status in [order.Submitted, order.Accepted]:
            #nothing to notify (since nothing executed)
            return

        #status of the completed order and for what price
        if order.status in [order.Completed]:
            if order.isbuy():
                #make note if buy
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                #make note if sell
                self.log("SELL EXECUTED {}".format(order.executed.price))

            #keep note of the bar of the most recent order, len(self) grows as the days pass
            self.bar_executed = len(self)

        #reset the current order after notified
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        #checks if there's still a pending order, if so, do nothing 
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    #buy order made if 3 bearish consecutive days
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            #we choose to sell after 5 days of most recent buy order
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATED {}'.format(self.dataclose[0])) 
                #we use self.order to keep track of status of order  
                self.order = self.sell()
