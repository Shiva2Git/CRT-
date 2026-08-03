import os
import pandas as pd


def create_folder(folder_path):
    """
    Create folder if it doesn't exist.
    """
    os.makedirs(folder_path, exist_ok=True)


def read_csv(file_path):
    """
    Read CSV safely.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}")
        print(e)
        return None


def save_csv(df, file_path):
    """
    Save DataFrame to CSV.
    """
    try:
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        print(e)
        return False


def clean_dataframe(df):
    """
    Remove incomplete OHLC rows.
    """

    df = df.dropna(
        subset=[
            "Open",
            "High",
            "Low",
            "Close"
        ]
    )

    df.reset_index(drop=True, inplace=True)

    return df


def validate_dataframe(df):
    """
    Check required columns exist.
    """

    columns = [
        "Open",
        "High",
        "Low",
        "Close"
    ]

    for col in columns:

        if col not in df.columns:

            return False

    return True


def last_two_candles(df):
    """
    Return last two completed candles.
    """

    df = clean_dataframe(df)

    if len(df) < 2:
        return None, None

    return df.iloc[-2], df.iloc[-1]


def print_title(title):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def percentage(value1, value2):

    if value2 == 0:
        return 0

    return round((value1 / value2) * 100, 2)


def format_price(price):

    return round(float(price), 2)


def candle_body(candle):

    return abs(
        float(candle["Close"]) -
        float(candle["Open"])
    )


def candle_range(candle):

    return (
        float(candle["High"]) -
        float(candle["Low"])
    )


def upper_wick(candle):

    return (
        float(candle["High"]) -
        max(
            float(candle["Open"]),
            float(candle["Close"])
        )
    )


def lower_wick(candle):

    return (
        min(
            float(candle["Open"]),
            float(candle["Close"])
        ) -
        float(candle["Low"])
    )