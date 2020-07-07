from src.SETUP import tradeapi, ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL


# instantiate REST API

class PaperBot:
    def __init__(self):
        self.alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL, api_version='v2')
        self.conn = tradeapi.stream2.StreamConn(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL)


# obtain account information
bd = PaperBot()
account = bd.alpaca.get_account()

print(account)
