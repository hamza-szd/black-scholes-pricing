import streamlit as st 
import numpy as np
import plotly.graph_objects as graph_objects
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns
from numpy import log, sqrt, exp
from scipy.stats import norm 
from BSModel import BlackScholes

#Semantic Page Layout: 
st.set_page_config(
    page_title="Dynamic Black-Scholes Option Pricing Model", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="💸",

)

#CSS Styling for the Sreamlit page
st.markdown("""
    <style>
    .metric-container {
        display: flex; 
        justify-content: center;
        align-items: center;
        padding: 8px; 
        width: auto; 
        margin: 0 auto; 
    }

    .call { /*For the custom call pricing class*/
        background-color: #90ee90; 
        color: black; 
        margin-right: 10px;
        border-radius: 10px;
    }

    .put { /*For the custom put pricing class*/
        background-color: #ffcccb;
        color: black; 
        border-radius: 10px; 
    }

    .value {
        font-size: 1.5rem; 
        font-weight: bold;
        margin: 0;
    }

    .label { /*For the label class*/
        font-size: 1rem;
        margin-bottom: 4px;
    }
</style>""", unsafe_allow_html=True)

#Sidebar configuration
with st.sidebar: 
    st.title("💸 Black-Scholes Options")
    st.write("By: Hamza Shahzad")

    spot_price = st.number_input("Current Asset Price:", value = 100.0)
    strike = st.number_input("Strike Price: ", value = 100.0)
    time_to_maturity = st.number_input("Time to Maturity (in Years)", value =1.0)
    volatility = st.number_input("Volatility (Stdev): ", value =0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

    st.markdown("---")
    recalculate_btn = st.button("Recompute Heatmap")
    spot_min = st.number_input("Min. Spot Price", min_value = 0.01, value = spot_price*0.8, step=0.01)
    spot_max = st.number_input("Max. Spot Price", min_value=0.01, value=spot_price*1.2, step=0.01)
    vol_min = st.slider('Min. Volatility', min_value = 0.01, max_value =1.0, value = volatility*0.5, step=0.01)
    vol_max = st.slider('Max. Volatility', min_value = 0.01, max_value =1.00, value = volatility*1.5, step=0.01 )
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

def heatmap(riskless_rate, 
            time_to_maturity,
             strike, 
             vol_range, 
             spot_range): 
    #Establish zero matrices with the corresponding dimensions
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    call_prices = np.zeros((len(vol_range), len(spot_range)))

    #Iterate over each linearly spaced volatility/spot ranges
    for i, spot in enumerate(spot_range):
        for j, vol in enumerate(vol_range): 
            #Compute BS Option pricings
            bs_model = BlackScholes(spot, vol, riskless_rate, strike, time_to_maturity)
            call_price, put_price = bs_model.compute_prices();
            #Assign to corresponding cell in the price matrix
            call_prices[i, j] = call_price 
            put_prices[i,j] = put_price 

    #Plotting Call Price Heatmap
    call_figure, call_axis = plt.subplots(figsize=(10,8))
    sns.heatmap(call_prices, xticklabels = np.round(vol_range,2), yticklabels= np.round(spot_range,2), annot=True, fmt= ".2f", cmap="viridis", ax=call_axis)
    call_axis.set_title("CALL")
    call_axis.set_xlabel("Volatility")
    call_axis.set_ylabel("Spot Price")

    #TODO: change the cmap to a P&L red-green mapping
    #Plotting Plot Price Heatmap
    put_figure, put_axis = plt.subplots(figsize=(10,8))
    sns.heatmap(put_prices, xticklabels=np.round(vol_range,2), yticklabels=np.round(spot_range,2), annot=True, cmap="viridis", ax=put_axis)
    put_axis.set_title("PUT")
    put_axis.set_xlabel('Volatility')
    put_axis.set_xlabel('Put Price')

    return call_figure, put_figure


#Main page display 
st.title("Black-Scholes Options Pricing Model")

#Instantiate a dictionary of inputs from the sidebar
data = {
    "Current Asset Price": [spot_price],
    "Strike Price": [strike],
    "Time to Maturity (in Years)": [time_to_maturity], 
    "Volatility (St-dev)": [volatility], 
    "Risk-Free Interest Rate": [interest_rate]
}

#Create a table to display paramterized data at the top of the page
data_frame = pd.DataFrame(data)
st.table(data_frame)

#Create containers of option price computed with those parameters
#TODO: Reorder parameters for positional argument passing
call_price, put_price = BlackScholes(spot_price, volatility, interest_rate, strike, time_to_maturity).compute_prices()
call, put = st.columns([1,1], gap="small")

with call: 
    #Custom class for the Call Pricing
    st.markdown(f"""
    <div class="metric-container call">
        <div>
            <div class="label">Call Value</div>
            <div class="value">${call_price:.2f}</div>
        </div>
    </div>""", unsafe_allow_html=True)

with put: 
       #Custom class for the Put pricing
       st.markdown(f"""
    <div class="metric-container put">
        <div>
            <div class="label">Put Value</div>
            <div class="value">${put_price:.2f}</div>
        </div>
    </div>""", unsafe_allow_html=True)
       
st.markdown("") #Vertical spacing
st.title("Interactive Option Pricing Heatmap")
st.info("""Explore how option pricing according to the Black-Scholes Fromula fluctuates
        with changes to Volatility and Spot prices. Model assumes constant strike price, maturity, 
        and interest rate.""")

#Containers for two heatmaps: 
call, put = st.columns([1,1], gap="small")
call_heatmap, put_heatmap = heatmap(interest_rate, time_to_maturity, strike, vol_range, spot_range)

with call: 
     st.subheader("Call Pricing Model")
     st.pyplot(call_heatmap)

with put: 
     st.subheader("Put Pricing Model")
     st.pyplot(put_heatmap)