from feature_extractor import (
    get_last_two_features,
    liquidity_sweep,
    inside_bar,
    outside_bar,
    displacement
)


def crt_buy(df):
    """
    CRT BUY Pattern
    """

    c1, c2 = get_last_two_features(df)

    if c1 is None:
        return False, {}

    score = 0

    # --------------------------
    # Rule 1
    # Previous candle bearish
    # --------------------------
    if c1["bearish"]:
        score += 15

    # --------------------------
    # Rule 2
    # Previous candle displacement
    # --------------------------
    if displacement(c1):
        score += 20

    # --------------------------
    # Rule 3
    # Liquidity Sweep
    # --------------------------
    if liquidity_sweep(c1, c2):
        score += 20

    # --------------------------
    # Rule 4
    # Long lower wick
    # --------------------------
    if c2["lower_ratio"] >= 0.40:
        score += 15

    # --------------------------
    # Rule 5
    # Small body
    # --------------------------
    if c2["body_ratio"] <= 0.35:
        score += 10

    # --------------------------
    # Rule 6
    # Close inside previous candle
    # --------------------------
    if (
        c2["close"] > c1["low"]
        and
        c2["close"] < c1["high"]
    ):
        score += 10

    # --------------------------
    # Rule 7
    # Not Outside Bar
    # --------------------------
    if not outside_bar(c1, c2):
        score += 5

    # --------------------------
    # Rule 8
    # Upper wick small
    # --------------------------
    if c2["upper_ratio"] <= 0.25:
        score += 5

    matched = score >= 70

    details = {

        "Pattern": "CRT BUY",

        "Score": score,

        "Matched": matched,

        "Previous Candle": c1,

        "Current Candle": c2

    }

    return matched, details


def crt_sell(df):
    """
    CRT SELL Pattern
    """

    c1, c2 = get_last_two_features(df)

    if c1 is None:
        return False, {}

    score = 0

    # Previous candle bullish
    if c1["bullish"]:
        score += 15

    # Displacement
    if displacement(c1):
        score += 20

    # Liquidity sweep above previous high
    if c2["high"] > c1["high"]:
        score += 20

    # Long upper wick
    if c2["upper_ratio"] >= 0.40:
        score += 15

    # Small body
    if c2["body_ratio"] <= 0.35:
        score += 10

    # Close inside previous candle
    if (
        c2["close"] < c1["high"]
        and
        c2["close"] > c1["low"]
    ):
        score += 10

    # Not outside bar
    if not outside_bar(c1, c2):
        score += 5

    # Lower wick small
    if c2["lower_ratio"] <= 0.25:
        score += 5

    matched = score >= 70

    details = {

        "Pattern": "CRT SELL",

        "Score": score,

        "Matched": matched,

        "Previous Candle": c1,

        "Current Candle": c2

    }

    return matched, details


if __name__ == "__main__":

    import pandas as pd

    df = pd.read_csv("data/3BBLACKBIO.csv")

    buy, buy_details = crt_buy(df)

    sell, sell_details = crt_sell(df)

    print()

    print("BUY")

    print(buy_details)

    print()

    print("SELL")

    print(sell_details)