import os
import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import (
    CSV_FILE,
    DATA_FOLDER,
    PERIOD,
    INTERVAL,
    MAX_WORKERS
)

from utils import clean_dataframe


def download_stock(symbol):

    try:

        ticker = symbol + ".NS"

        df = yf.download(
            ticker,
            period=PERIOD,
            interval=INTERVAL,
            progress=False,
            auto_adjust=False,
            threads=False
        )

        if df.empty:
            return False

        # Fix MultiIndex columns (new yfinance versions)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.reset_index(inplace=True)

        df = clean_dataframe(df)

        if len(df) < 20:
            return False

        file = os.path.join(DATA_FOLDER, f"{symbol}.csv")

        df.to_csv(file, index=False)

        return True

    except Exception as e:

        print(symbol, e)

        return False


def worker(row):

    symbol = str(row["SYMBOL"]).strip()

    ok = download_stock(symbol)

    return symbol, ok


def download_all():

    stocks = pd.read_csv(CSV_FILE)

    total = len(stocks)

    success = 0

    failed = []

    print(f"\nDownloading {total} Stocks...\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = []

        for _, row in stocks.iterrows():

            futures.append(executor.submit(worker, row))

        completed = 0

        for future in as_completed(futures):

            completed += 1

            symbol, ok = future.result()

            if ok:

                success += 1

                print(f"[{completed}/{total}] ✅ {symbol}")

            else:

                failed.append(symbol)

                print(f"[{completed}/{total}] ❌ {symbol}")

    print("\n==========================")
    print("Download Completed")
    print("==========================")

    print("Success :", success)
    print("Failed  :", len(failed))

    if failed:

        print("\nFailed Stocks")

        for stock in failed:

            print(stock)


if __name__ == "__main__":

    download_all()