import streamlit as st
import pandas as pd
import os

from data import download_all
from scanner import scan_all
from chart_generator import generate_from_csv
from config import (
    OUTPUT_FOLDER,
    CHART_FOLDER
)

st.set_page_config(
    page_title="NSE CRT Scanner",
    page_icon="📈",
    layout="wide"
)

st.title("📈 NSE CRT Scanner")
st.write("Find CRT Buy & Sell patterns in NSE Stocks")

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("Menu")

download_btn = st.sidebar.button("📥 Download Data")
scan_btn = st.sidebar.button("🔍 Scan Stocks")
chart_btn = st.sidebar.button("📊 Generate Charts")

# ----------------------------
# Download
# ----------------------------

if download_btn:

    with st.spinner("Downloading Daily Data..."):

        download_all()

    st.success("Download Completed")

# ----------------------------
# Scan
# ----------------------------

if scan_btn:

    with st.spinner("Scanning Stocks..."):

        buy_df, sell_df = scan_all()

    st.success("Scan Completed")

# ----------------------------
# Generate Charts
# ----------------------------

if chart_btn:

    buy_file = os.path.join(
        OUTPUT_FOLDER,
        "crt_buy.csv"
    )

    if os.path.exists(buy_file):

        with st.spinner("Generating Charts..."):

            generate_from_csv(buy_file)

        st.success("Charts Generated")

# ----------------------------
# BUY Signals
# ----------------------------

buy_file = os.path.join(
    OUTPUT_FOLDER,
    "crt_buy.csv"
)

if os.path.exists(buy_file):

    st.header("CRT BUY")

    buy = pd.read_csv(buy_file)

    st.dataframe(
        buy,
        use_container_width=True
    )

    stock = st.selectbox(
        "Select Stock",
        buy["Symbol"]
    )

    image = os.path.join(
        CHART_FOLDER,
        stock + ".png"
    )

    if os.path.exists(image):

        st.image(
            image,
            caption=stock,
            use_container_width=True
        )

# ----------------------------
# SELL Signals
# ----------------------------

sell_file = os.path.join(
    OUTPUT_FOLDER,
    "crt_sell.csv"
)

if os.path.exists(sell_file):

    st.header("CRT SELL")

    sell = pd.read_csv(sell_file)

    st.dataframe(
        sell,
        use_container_width=True
    )

st.write("---")

st.write("Developed by Shiva 🚀")