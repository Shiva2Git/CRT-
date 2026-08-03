import os
import pandas as pd

from config import DATA_FOLDER, OUTPUT_FOLDER
from pattern_detector import crt_buy, crt_sell


def scan_all():

    buy_results = []
    sell_results = []

    files = sorted([
        f for f in os.listdir(DATA_FOLDER)
        if f.endswith(".csv")
    ])

    total = len(files)

    print(f"\nScanning {total} Stocks...\n")

    for index, file in enumerate(files):

        symbol = file.replace(".csv", "")

        print(f"[{index+1}/{total}] {symbol}")

        try:

            path = os.path.join(DATA_FOLDER, file)

            df = pd.read_csv(path)

            # ---------------- BUY ----------------

            matched, details = crt_buy(df)

            if matched:

                current = details["Current Candle"]

                buy_results.append({

                    "Symbol": symbol,

                    "Pattern": "CRT BUY",

                    "Score": details["Score"],

                    "Open": current["open"],

                    "High": current["high"],

                    "Low": current["low"],

                    "Close": current["close"]

                })

            # ---------------- SELL ----------------

            matched, details = crt_sell(df)

            if matched:

                current = details["Current Candle"]

                sell_results.append({

                    "Symbol": symbol,

                    "Pattern": "CRT SELL",

                    "Score": details["Score"],

                    "Open": current["open"],

                    "High": current["high"],

                    "Low": current["low"],

                    "Close": current["close"]

                })

        except Exception as e:

            print(symbol, e)

    # ---------------- BUY CSV ----------------

    buy_df = pd.DataFrame(buy_results)

    if not buy_df.empty:

        buy_df = buy_df.sort_values(
            by="Score",
            ascending=False
        )

        buy_df.to_csv(
            os.path.join(
                OUTPUT_FOLDER,
                "crt_buy.csv"
            ),
            index=False
        )

    # ---------------- SELL CSV ----------------

    sell_df = pd.DataFrame(sell_results)

    if not sell_df.empty:

        sell_df = sell_df.sort_values(
            by="Score",
            ascending=False
        )

        sell_df.to_csv(
            os.path.join(
                OUTPUT_FOLDER,
                "crt_sell.csv"
            ),
            index=False
        )

    print("\n==========================")
    print("Scan Completed")
    print("==========================")

    print("BUY Signals :", len(buy_df))
    print("SELL Signals:", len(sell_df))

    return buy_df, sell_df


if __name__ == "__main__":

    buy, sell = scan_all()

    print("\n========== BUY ==========\n")

    print(buy.head(20))

    print("\n========== SELL ==========\n")

    print(sell.head(20))