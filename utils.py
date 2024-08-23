import streamlit as st
from styles import help_icon
import pandas as pd
import requests

descriptions = {
     "Current Asset Price": "The current price of the underlying asset (e.g. the current stock price)",
     "Strike Price": "The exercise price at which you may purchase the asset at a future date",
     "Time to Maturity": "Years until option maturity (the exercise deadline).",
     "Volatility": "Volatility of the underlying asset (Standard deviation of returns)",
     "Risk-Free Interest Rate": "Risk-Free Market Rate (e.g. 10 year US Treasury Bond Returns)",
     "Current Put Price": "The current price in the market to purchase the put option in question. Will be used for a P&L (Profit and Loss) analysis based on the Black-Scholes calculation of how valuable the option is.",
     "Current Call Price": "The current price in the market to purchase the call option in question. Will be used for a P&L (Profit and Loss) analysis based on the Black-Scholes calculation of how valuable the option is."


}



def render_field(label, value, key):
    # Render label and help icon on the same line with the icon aligned to the right
    st.markdown(f"""
    <div class="fields">
        {label}{help_icon(descriptions[label])}""", unsafe_allow_html=True)
    return st.number_input("", value=value, key=key)

def sp500_map(): 
    ticker_df = pd.read_csv("sp500ticker.csv", header=None)
    names_df = pd.read_csv("sp500name.csv", header=None)

    return dict(zip(names_df[0], ticker_df[0]))


def fetch_close(ticker):
    close_price = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices/?token=be4f69d69686dc259aa7e10594cbb22c3ac40df6").json()[0]["close"]
    return close_price
