from src.SETUP import tradeapi, ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL
from tkinter import *
import threading, time

# instantiate REST API

HEADER = {
    'APCA-API-KEY-ID': ALPACA_API_KEY,
    'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
}


def start_script(bd):
    ticker = input("Which stock would you like to analyze? (input: CAPITALIZED TICKER SYMBOL)")
    # COLLECTING BARSET DATA
    barset = bd.alpaca.get_barset(ticker, '1D', limit=30)

    high = barset[ticker][0].h
    low = barset[ticker][0].l
    for candle in barset[ticker]:
        if candle.h > high:
            high = candle.h
        elif candle.l < low:
            low = candle.l
    range_size = high - low

    print("Monthly High: " + str(high))
    print("Monthly Low: " + str(low))
    print("Monthly Range: " + str(range_size))


class PaperBot:
    def __init__(self):
        self.alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL, api_version='v2')
        # self.conn = tradeapi.stream2.StreamConn(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL)
        self.stonks = []

        self.root = Tk()
        # INIT GUI
        Button(self.root, text="Button", padx=50, command=self.addtotradinglist, fg="#FF4500").grid(row=0, column=0)
        self.input = Entry(self.root, width=50).grid(row=1, column=0)
        self.root.mainloop()

    def addtotradinglist(self):
        self.stonks.append(self.input.get())


bd = PaperBot()

# account = bd.alpaca.get_account()
# print("You currently have: $" + account.cash)

# CREATING GUI


# ALPACA ACCOUNT


# SCRIPT


# tsla = bd.alpaca.alpha_vantage.historic_quotes('TSLA', adjusted=True, output_format='json', cadence='weekly')

# use account.x to retrieve certain account information
# print(tsla)
