from numpy import log, sqrt, exp
from scipy.stats import norm

class BlackScholes:
    def __init__(
            self, 
            spot_price: float, 
            volatility: float,
            riskless_rate: float, 
            strike: float,
            time_to_maturity: float,
    ): 
        self.spot_price = spot_price
        self.volatility = volatility #Standard deviation of returns
        self.riskless_rate = riskless_rate #in decimal format
        self.strike = strike
        self.time_to_maturity = time_to_maturity #In years
    
    def compute_prices(self): 
        '''Implements the Black-Scholes Formula for
        Call and Put pricing'''
        S = self.spot_price
        X = self.strike
        T = self.time_to_maturity
        R = self.riskless_rate
        V = self.volatility

        #To be passed into Norm function
        d1 = (log(S/X) + (R + 0.5*V**2)*T)/(V*sqrt(T))
        d2 = d1 - V*sqrt(T)

        call_price = S * norm.cdf(d1) - X*exp(-(R*T))*norm.cdf(d2)
        put_price = X*(exp(-(R*T)))*norm.cdf(-d2) - S*norm.cdf(-d1)

        return [call_price, put_price]