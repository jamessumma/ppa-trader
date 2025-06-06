import os
import yaml
import pandas as pd
from alpaca_trade_api.rest import REST
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

with open("data-center/config.yaml", "r") as file:
    config = yaml.safe_load(file)

SYMBOLS = config["symbols"]
TIMEFRAME = config.get("timeframe", "1Min")
DAYS_BACK = config.get("days_back", 7)
DATA_DIR = "data-center/pre-processed-data"
FEED_TYPE = config.get("feed", "iex")
os.makedirs(DATA_DIR, exist_ok=True)

# Alpaca Credentials
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

if not API_KEY or not API_SECRET:
    raise ValueError("Missing Alpaca API credentials in environment variables.")

api = REST(API_KEY, API_SECRET, BASE_URL)

# Date Range
days_back = config.get("date_range", {}).get("days_back", 7)
end = pd.Timestamp.now(tz="America/New_York")
start = end - pd.Timedelta(days=days_back)

# Download + Save Each Symbol
for symbol in SYMBOLS:
    print(f"Downloading: {symbol}...")
    bars = api.get_bars(
        symbol,
        timeframe=TIMEFRAME,
        start=start.isoformat(),
        end=end.isoformat(),
        adjustment="raw",
        feed=FEED_TYPE
    ).df


    if bars.empty:
        print(f"No data for {symbol}")
        continue

    bars = bars.reset_index()
    bars.to_csv(f"{DATA_DIR}/{symbol}.csv", index=False)
    print(f"Saved: {symbol}.csv")

# Signal Done
done_path = os.path.join(DATA_DIR, config["output"].get("done_signal", ".done"))
with open(done_path, "w") as f:
    f.write("scraper complete\n")

print("✅ Data scraping complete.")