import os
import pandas as pd
import mplfinance as mpf

from config import (
    DATA_FOLDER,
    CHART_FOLDER,
    NUMBER_OF_CANDLES,
    CHART_STYLE
)


def generate_chart(symbol):

    file = os.path.join(DATA_FOLDER, f"{symbol}.csv")

    if not os.path.exists(file):
        return False

    try:

        df = pd.read_csv(file)

        df = df.dropna(
            subset=["Open", "High", "Low", "Close"]
        )

        if len(df) < NUMBER_OF_CANDLES:
            return False

        df["Date"] = pd.to_datetime(df["Date"])

        df.set_index("Date", inplace=True)

        chart = df.tail(NUMBER_OF_CANDLES)

        save_path = os.path.join(
            CHART_FOLDER,
            f"{symbol}.png"
        )

        mpf.plot(

            chart,

            type="candle",

            style=CHART_STYLE,

            volume=True,

            mav=(20,),

            figsize=(12,8),

            tight_layout=True,

            savefig=dict(

                fname=save_path,

                dpi=200,

                bbox_inches="tight"

            )

        )

        return True

    except Exception as e:

        print(symbol, e)

        return False


def generate_from_csv(csv_file):

    stocks = pd.read_csv(csv_file)

    total = len(stocks)

    print(f"\nGenerating {total} Charts\n")

    success = 0

    for i, row in stocks.iterrows():

        symbol = row["Symbol"]

        print(f"[{i+1}/{total}] {symbol}")

        if generate_chart(symbol):

            success += 1

    print()

    print("======================")

    print("Finished")

    print("======================")

    print("Charts :", success)