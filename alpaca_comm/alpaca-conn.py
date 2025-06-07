from alpaca_trade_api.rest import REST
import os
from dotenv import load_dotenv
load_dotenv()

# Alpaca Credentials
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

if not API_KEY or not API_SECRET:
    raise ValueError("Missing Alpaca API credentials in environment variables.")

class AlpacaConn:

    def __init__(self):
        self.api = REST(API_KEY, API_SECRET, BASE_URL)