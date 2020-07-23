from src.SETUP import tradeapi, ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL, BARS_URL
import requests

# instantiate REST API

HEADER = {
    'APCA-API-KEY-ID': ALPACA_API_KEY,
    'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
}


class PaperBot:
    def __init__(self):
        self.alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL, api_version='v2')
        # self.conn = tradeapi.stream2.StreamConn(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL)


# ALPACA ACCOUNT
bd = PaperBot()
account = bd.alpaca.get_account()

# SCRIPT
print("You currently have: $" + account.cash)
ticker = input("Which stock would you like to analyze? (input: CAPITALIZED TICKER SYMBOL)")

# COLLECTING BARSET DATA
barset = bd.alpaca.get_barset(ticker, '1D', limit=30)
barset2 = barset[ticker]

high = barset2[0].h
low = barset2[0].l
for candle in barset2:
    if candle.h > high:
        high = candle.h
    elif candle.l < low:
        low = candle.l
range_size = high - low

print("Monthly High: " + str(high))
print("Monthly Low: " + str(low))
print("Monthly Range: " + str(range_size))

tsla = bd.alpaca.alpha_vantage.historic_quotes('TSLA', adjusted=True, output_format='json', cadence='weekly')

# use account.x to retrieve certain account information
#print(tsla)
#print(barset['AAPL'][0].c)
