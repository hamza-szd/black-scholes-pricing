import streamlit as st 
import numpy as np
import pandas as pd
from BSModel import BlackScholes
from styles import apply_css, help_icon
from heatmap import heatmap, heatmap_PNL
from utils import render_field, sp500_map, fetch_close

#Semantic Page Layout: 
st.set_page_config(
    page_title="Dynamic Black-Scholes Options P&L Models", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="💸",
)

apply_css() 


with st.sidebar:
    st.title("💸 Black-Scholes Parameters")
    st.write("By: Hamza Shahzad")

    st.button("Option Parameters")

    ticker_map = sp500_map()
    Choice = st.sidebar.selectbox("Current Asset Price", list(ticker_map.keys()))

    S = fetch_close(ticker_map[Choice])
    #S = render_field("Current Asset Price", value = 100.0, key="S")
    X = render_field("Strike Price", value = 200.0, key="X")
    T = render_field("Time to Maturity", value = 1.0, key="T")
    V = render_field("Volatility", value = 0.2, key="V")
    R = render_field("Risk-Free Interest Rate", value = 0.2, key="R")
    
    st.markdown("---")
    st.button("Current Option Price")
    put_price = render_field("Current Put Price", value = 100.0, key="put_price")
    call_price = render_field("Current Call Price", value = 100.0, key="call_price")

    st.markdown("---")
    recalculate_btn = st.button("Heatmap Parameters")
    spot_min = st.number_input("Min. Spot Price", min_value = 0.01, value = S*0.8, step=0.01)
    spot_max = st.number_input("Max. Spot Price", min_value=0.01, value=S*1.2, step=0.01)
    vol_min = st.slider('Min. Volatility', min_value = 0.01, max_value =1.0, value = V*0.5, step=0.01)
    vol_max = st.slider('Max. Volatility', min_value = 0.01, max_value =1.00, value = V*1.5, step=0.01 )

    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)


#Main page display 
st.title("💸 Black-Scholes Options Pricing Models")

#Instantiate a dictionary of inputs from the sidebar
data = {
    "Current Asset Price": S,
    "Strike Price": X,
    "Time to Maturity (in Years)": T, 
    "Volatility (St-dev)": V, 
    "Risk-Free Interest Rate": R
}

#Create a table to display parameterized data at the top of the page
data_frame = pd.DataFrame(data, index=["Value"])

# Define a Styler object with formatting
data_frame = pd.DataFrame(data, index=["Value"])

# Define a Styler object with formatting
styled_df = data_frame.style.format("{:.2f}").set_table_styles({
    'Current Asset Price': [{'selector': 'td', 'props': [('text-align', 'center'), ('padding', '10px')]}],
    'Strike Price': [{'selector': 'td', 'props': [('text-align', 'center'), ('padding', '10px')]}],
    'Time to Maturity (in Years)': [{'selector': 'td', 'props': [('text-align', 'center'), ('padding', '10px')]}],
    'Volatility (St-dev)': [{'selector': 'td', 'props': [('text-align', 'center'), ('padding', '10px')]}],
    'Risk-Free Interest Rate': [{'selector': 'td', 'props': [('text-align', 'center'), ('padding', '10px')]}]
})

# Display the styled DataFrame in Streamlit
st.dataframe(styled_df)
#Create containers of option price computed with those parameters
#TODO: Reorder parameters for positional argument passing
call_price, put_price = BlackScholes(S, V, R, X, T).compute_prices()
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
       
st.markdown("") 
st.title("Option Value Model")
st.info("""Explore how fluctuations in volatility and spot price of the underlying asset
        can affect the value of the option specified in the sidebar according to the Black-Scholes
        Equation.""")

#Containers for two heatmaps: 
call, put = st.columns([1,1], gap="small")
call_heatmap, put_heatmap = heatmap(
     riskless_rate = R,
     time_to_maturity= T,
     strike = X,
     vol_range = vol_range,
     spot_range = spot_range
     )

with call: 
     st.subheader("Call Pricing Model")
     st.pyplot(call_heatmap)


with put: 
     st.subheader("Put Pricing Model")
     st.pyplot(put_heatmap)

st.markdown("") 
st.title("Option P&L Model")
st.info("""Explore how fluctuations in volatility and spot price of the underlying asset
        can affect the Profit or Loss margins on the option specified in the sidebar. Net profit
        is computed as: Market Option Price - Option Value (according to the B.S. Equation)""")

#Containers for the PNL Heatmaps
callPNL, putPNL = st.columns([1,1], gap="small")
call_PNL_heatmap, put_PNL_heatmap = heatmap_PNL(
     riskless_rate = R,
     time_to_maturity=T,
     strike = X,
     vol_range = vol_range,
     spot_range = spot_range,
     put_price= put_price,
     call_price=call_price
     )

with callPNL: 
     st.subheader("Call P&L")
     st.pyplot(call_PNL_heatmap)


with putPNL: 
     st.subheader("Put P&L")
     st.pyplot(put_PNL_heatmap)