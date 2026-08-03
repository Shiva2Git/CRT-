import pandas as pd


def analyze_last_two_candles(df):
    """
    Analyze the last two completed daily candles.

    Returns:
        matched (bool)
        details (dict)
    """

    # Remove incomplete candles
    df = df.dropna(subset=["Open", "High", "Low", "Close"])

    if len(df) < 2:
        return False, {}

    c1 = df.iloc[-2]
    c2 = df.iloc[-1]

    # -----------------------------
    # Candle 1
    # -----------------------------
    o1 = float(c1["Open"])
    h1 = float(c1["High"])
    l1 = float(c1["Low"])
    cl1 = float(c1["Close"])

    body1 = abs(cl1 - o1)
    range1 = h1 - l1

    # -----------------------------
    # Candle 2
    # -----------------------------
    o2 = float(c2["Open"])
    h2 = float(c2["High"])
    l2 = float(c2["Low"])
    cl2 = float(c2["Close"])

    body2 = abs(cl2 - o2)
    range2 = h2 - l2

    lower_wick = min(o2, cl2) - l2
    upper_wick = h2 - max(o2, cl2)

    score = 0

    # ---------------------------------
    # Rule 1 : Large previous candle
    # ---------------------------------
    if range1 > 0 and body1 >= range1 * 0.50:
        score += 20

    # ---------------------------------
    # Rule 2 : Small second candle
    # ---------------------------------
    if range2 > 0 and body2 <= range2 * 0.35:
        score += 20

    # ---------------------------------
    # Rule 3 : Long lower wick
    # ---------------------------------
    if body2 > 0 and lower_wick >= body2 * 1.5:
        score += 20

    # ---------------------------------
    # Rule 4 : Small upper wick
    # ---------------------------------
    if body2 > 0 and upper_wick <= body2 * 2:
        score += 10

    # ---------------------------------
    # Rule 5 : Liquidity Sweep
    # ---------------------------------
    if l2 <= l1:
        score += 10

    # ---------------------------------
    # Rule 6 : Close inside previous range
    # ---------------------------------
    if l1 <= cl2 <= h1:
        score += 10

    # ---------------------------------
    # Rule 7 : Previous candle bearish
    # ---------------------------------
    if cl1 < o1:
        score += 5

    # ---------------------------------
    # Rule 8 : Gap between opens
    # ---------------------------------
    if abs(o2 - cl1) <= body1:
        score += 5

    matched = score >= 70

    return matched, {

        "Score": score,

        "Candle1_Open": o1,
        "Candle1_High": h1,
        "Candle1_Low": l1,
        "Candle1_Close": cl1,

        "Candle2_Open": o2,
        "Candle2_High": h2,
        "Candle2_Low": l2,
        "Candle2_Close": cl2,

        "Body1": round(body1, 2),
        "Body2": round(body2, 2),

        "Range1": round(range1, 2),
        "Range2": round(range2, 2),

        "LowerWick": round(lower_wick, 2),
        "UpperWick": round(upper_wick, 2)
    }

