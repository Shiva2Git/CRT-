import pandas as pd
from utils import (
    candle_body,
    candle_range,
    upper_wick,
    lower_wick
)


def extract_features(candle):
    """
    Extract features from a single candle.
    """

    body = candle_body(candle)
    total_range = candle_range(candle)

    if total_range == 0:
        total_range = 0.0001

    upper = upper_wick(candle)
    lower = lower_wick(candle)

    bullish = float(candle["Close"]) > float(candle["Open"])
    bearish = float(candle["Close"]) < float(candle["Open"])

    return {

        "open": float(candle["Open"]),
        "high": float(candle["High"]),
        "low": float(candle["Low"]),
        "close": float(candle["Close"]),

        "body": round(body,2),
        "range": round(total_range,2),

        "body_ratio": round(body/total_range,4),
        "upper_ratio": round(upper/total_range,4),
        "lower_ratio": round(lower/total_range,4),

        "upper_wick": round(upper,2),
        "lower_wick": round(lower,2),

        "bullish": bullish,
        "bearish": bearish
    }


def get_last_two_features(df):
    """
    Return feature dictionaries for last two candles.
    """

    df = df.dropna(
        subset=[
            "Open",
            "High",
            "Low",
            "Close"
        ]
    )

    if len(df) < 2:
        return None, None

    candle1 = df.iloc[-2]
    candle2 = df.iloc[-1]

    feature1 = extract_features(candle1)
    feature2 = extract_features(candle2)

    return feature1, feature2


def liquidity_sweep(candle1, candle2):
    """
    Did current candle sweep previous low?
    """

    return candle2["low"] < candle1["low"]


def inside_bar(candle1, candle2):

    return (

        candle2["high"] <= candle1["high"]

        and

        candle2["low"] >= candle1["low"]

    )


def outside_bar(candle1, candle2):

    return (

        candle2["high"] > candle1["high"]

        and

        candle2["low"] < candle1["low"]

    )


def gap_up(candle1, candle2):

    return candle2["open"] > candle1["high"]


def gap_down(candle1, candle2):

    return candle2["open"] < candle1["low"]


def displacement(candle):

    return candle["body_ratio"] >= 0.60


if __name__ == "__main__":

    df = pd.read_csv("data/3BBLACKBIO.csv")

    c1, c2 = get_last_two_features(df)

    print()

    print(c1)

    print()

    print(c2)

    print()

    print("Liquidity Sweep :", liquidity_sweep(c1,c2))

    print("Inside Bar :", inside_bar(c1,c2))

    print("Outside Bar :", outside_bar(c1,c2))

    print("Gap Up :", gap_up(c1,c2))

    print("Gap Down :", gap_down(c1,c2))

    print("Displacement :", displacement(c1))