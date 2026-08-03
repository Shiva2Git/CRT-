import os
import pandas as pd
import yfinance as yf

DATA_FOLDER = "data"

os.makedirs(DATA_FOLDER, exist_ok=True)


def download_stock(symbol):

    try:

        ticker = symbol + ".NS"

        df = yf.download(
            ticker,
            period="90d",
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False
        )

        if df.empty:
            return False

        # Fix MultiIndex columns (new yfinance versions)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.to_csv(f"{DATA_FOLDER}/{symbol}.csv")

        print(f"Downloaded : {symbol}")

        return True

    except Exception as e:

        print(symbol, e)

        return False


def download_all(csv_file):

    stocks = pd.read_csv(csv_file)

    total = len(stocks)

    print(f"Total Stocks : {total}")

    success = 0

    for i, row in stocks.iterrows():

        symbol = str(row["SYMBOL"]).strip()

        print(f"[{i+1}/{total}] {symbol}")

        if download_stock(symbol):
            success += 1

    print(f"\nDownloaded {success}/{total}")

