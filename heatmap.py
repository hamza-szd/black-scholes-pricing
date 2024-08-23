import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from BSModel import BlackScholes

#Heatmap of Black-Scholes calculated options value with fluctuating spot price and volatility
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
            call_price, put_price = bs_model.compute_prices()
            #Assign to corresponding cell in the price matrix
            call_prices[i, j] = call_price 
            put_prices[i,j] = put_price 

    #Plotting Call Price Heatmap
    call_figure, call_axis = plt.subplots(figsize=(10,8))
    sns.heatmap(call_prices, xticklabels = np.round(vol_range,2), yticklabels= np.round(spot_range,2), annot=True, fmt= ".2f", cmap="viridis", ax=call_axis)
    call_axis.set_title("CALL")
    call_axis.set_xlabel("Volatility")
    call_axis.set_ylabel("Spot Price")

    #Plotting Plot Price Heatmap
    put_figure, put_axis = plt.subplots(figsize=(10,8))
    sns.heatmap(put_prices, xticklabels=np.round(vol_range,2), yticklabels=np.round(spot_range,2), fmt= ".2f", annot=True, cmap="viridis", ax=put_axis)
    put_axis.set_title("PUT")
    put_axis.set_xlabel('Volatility')
    put_axis.set_xlabel('Put Price')

    return call_figure, put_figure

#Heatmap of Profit/Loss given a current market option price and varying spot price and volitility 
def heatmap_PNL(riskless_rate, 
            time_to_maturity,
             strike, 
             vol_range, 
             spot_range, 
             put_price, 
             call_price,): 
    #Establish zero matrices with the corresponding dimensions
    put_pnls = np.zeros((len(vol_range), len(spot_range)))
    call_pnls = np.zeros((len(vol_range), len(spot_range)))

    #Iterate over each linearly spaced volatility/spot ranges
    for i, spot in enumerate(spot_range):
        for j, vol in enumerate(vol_range): 
            #Compute BS Option pricings
            bs_model = BlackScholes(spot, vol, riskless_rate, strike, time_to_maturity)
            call_PNL, put_PNL = bs_model.compute_PNL(put_price, call_price)
            #Assign to corresponding cell in the price matrix
            call_pnls[i, j] = call_PNL
            put_pnls[i,j] = put_PNL

    #Plotting Call PNL Heatmap
    call_figure, call_axis = plt.subplots(figsize=(10,8))
    sns.heatmap(call_pnls, xticklabels = np.round(vol_range,2), yticklabels= np.round(spot_range,2), annot=True, fmt= ".2f", cmap= LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256) , ax=call_axis)
    call_axis.set_title("CALL P&L")
    call_axis.set_xlabel("Volatility")
    call_axis.set_ylabel("Spot Price")

    #Plotting Plot Price Heatmap
    put_figure, put_axis = plt.subplots(figsize=(10,8))
    sns.heatmap(put_pnls, xticklabels=np.round(vol_range,2), yticklabels=np.round(spot_range,2),fmt= ".2f", annot=True, cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256), ax=put_axis)
    put_axis.set_title("PUT P&L")
    put_axis.set_xlabel('Volatility')
    put_axis.set_xlabel('Put Price')

    return call_figure, put_figure