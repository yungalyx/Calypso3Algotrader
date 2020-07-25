from datetime import datetime
import backtrader as bt
import backtrader.indicators as btind
import math


class AllocationStrategy(bt.Strategy):
    params = (("BBandsPeriod", 20), ("Order_Percentage", 0.05))

    def log(self):
        pass

    def __init__(self):
        self.inds = dict()  # going to store indicators in dictionary for each stock ive added
        self.sma = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = btind.BollingerBands(d, period=self.params.BBandsPeriod)

    def market_uptrending(self, d):
        if self.inds[d].lines.mid[-10] < self.inds[d].lines.mid[-5]:
            return True
        else:
            return False

    def next(self):
        cash_on_hand = self.broker.get_cash()
        invest_amt = cash_on_hand * self.params.Order_Percentage
        # if today's price opened is below bband,

        for i, d in enumerate(self.datas):  # i refers to index, d refers to data object it is attached to
            dn = d._name

            # if the market is uptrending, we can buy dips
            if self.market_uptrending(d):
                # if close was below botlinger today and yesterday, enter trade
                if self.datas[i].close[0] < self.inds[d].lines.bot[0]:
                    if self.datas[i].close[-1] < self.inds[d].lines.bot[-1]:
                        self.size = math.floor(invest_amt / self.datas[i].close)
                        print("LONG: {} shares of {} at {}".format(self.size, dn, self.datas[i].close[0]))
                        self.buy(data=d, size=self.size)

                elif self.datas[i].close[0] > self.inds[d].lines.top[0]:
                    if self.datas[i].close[-1] > self.inds[d].lines.top[-1]:
                        print("CLOSE: {} shares of {} at {}".format(self.position.size, dn, self.datas[i].close[0]))
                        self.close(data=d)


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=20)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(1337.0)
    cerebro.broker.setcommission(commission=0.001)

    data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                     fromdate=datetime(2017, 1, 1),
                                     todate=datetime(2017, 12, 31))
    cerebro.adddata(data)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
