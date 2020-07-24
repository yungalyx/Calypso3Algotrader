from src.SETUP import tradeapi, ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL
from tkinter import *
import backtrader as bt
import datetime as dt
import matplotlib
import yfinance as yf

# instantiate REST API
HEADER = {
    'APCA-API-KEY-ID': ALPACA_API_KEY,
    'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
}

# COLLECTING DATA:
# i = self.alpaca.get_barset(ticker, timeframe='day', start=start, end=end).df[ticker]
# i = self.alpaca.alpha_vantage.historic_quotes(ticker, adjusted=True, output_format='csv')
# self.alpaca.alpha_vantage.intraday_quotes('tsla')


start = dt.datetime(2020, 1, 1)
end = dt.datetime.now()

cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']


class PaperBot:
    def __init__(self):
        self.alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL, api_version='v2')
        # self.conn = tradeapi.stream2.StreamConn(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL)
        self.stonks = []
        self.cerebro = bt.Cerebro()

        self.root = Tk()
        # INIT GUI
        self.input = Entry(self.root, width=50, borderwidth=3)
        self.input.grid(row=0, column=0)
        # command=Lambda: self.addtotradinglist(1)  <-- allows u to pass parameters on button click before running the function
        Button(self.root, text="Add a TICKER to stock list", padx=30, command=self.addtotradinglist, fg="#FF4500").grid(
            row=0, column=1)
        Button(self.root, text="Run backtest", padx=50, command=self.runbacktest).grid(row=3, column=0, columnspan=2)

        self.text = StringVar()
        self.text.set("Current List:")
        self.label = Label(self.root, textvariable=self.text).grid(row=2, column=0)
        self.root.mainloop()

    def addtotradinglist(self):
        try:
            self.alpaca.get_asset(self.input.get())
            self.stonks.append(self.input.get())
        except:
            print("not a valid asset / DNE")
            self.text.set("NOT A VALID TICKER SYMBOL")
        else:
            self.text.set("Current List: " + ", ".join(self.stonks))
        finally:
            self.input.delete(0, END)
            print(self.stonks)

    def runbacktest(self):
        # two ways to get data alpha vantage + alpaca barset
        for ticker in self.stonks:
            i = bt.feeds.YahooFinance(dataname=ticker, fromdate=start, todate=end)
            # i = yf.Ticker(ticker)
            # i = i.history(start=start, end=end)
            # print(i.head())
            self.cerebro.adddata(i)
        self.cerebro.run()
        self.cerebro.plot()


bd = PaperBot()

# account = bd.alpaca.get_account()
# print("You currently have: $" + account.cash)


# use account.x to retrieve certain account information
