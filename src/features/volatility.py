
#general libraries used 
import pandas as pd
import numpy as np


##################################################################
####                         Helpers                          ####
##################################################################
def roll_std(s, w):
        return s.rolling(window=w, min_periods=w).std()

def roll_sum(s, w):
        return s.rolling(window=w, min_periods=w).sum()




##################################################################
####                                                          ####
####                        1.1, 1.2                          ####
####               Volume Normalized returns                  ####
####                   +Volatility intraday                   ####
####                        + EWMA                            ####
####                                                          ####
##################################################################

def Vol_normalized(df):
    # the volume normalized return is very useful because it takes into account the context of what is going on 
    # in the market. i.e the market is very stable barely any movement and then a sudden rise by 0.5%, it is a breakout
    # but if the market is very noisy and very volatile and a move of 0.5% doesn't count as a move of 0.5% in the last scenario
    # so we feed it the 1, 5, 20, 60 and 90 of this indicator to give it broader market context
    
    # we start by making a copy of the main df so we don't mess with original data
    temp = df.copy()
    # sorting by timestamp to make sure everything good 
    temp = temp.sort_values("timestamp").reset_index(drop=True)

    # A tiny number to prevent "Division by Zero" errors
    epsilon = 1e-6

    # we need to split the data into days before using the rolling window on each
    #making sure everything is in UTC 
    temp['timestamp'] = pd.to_datetime(temp['timestamp'])
    if temp['timestamp'].dt.tz is None:
        temp['timestamp'] = temp['timestamp'].dt.tz_localize('UTC')
    else:
        temp['timestamp'] = temp['timestamp'].dt.tz_convert('UTC')

    #convert to local time
    temp['local_time'] = temp['timestamp'].dt.tz_convert('America/Los_Angeles')

    # making a new col as a datetime
    temp['date'] = temp['local_time'].dt.date

    # getting the log return for each bar, this will leave the first of each day empty
    # here .shift gets the row above by 1 geting the return
    temp['log_ret'] = temp.groupby('date')['close'].transform(lambda s: np.log(s / s.shift(1))).fillna(0.0)

    # the alpha for the EWMA
    alpha = 0.02 

    EWMA = temp.groupby('date')['log_ret'].transform(lambda s: s.shift(1).ewm(alpha=0.02, adjust=False).std())
    
    # Volatility per day only
    # intraday volatility is essentially the standard deviation because we are getting basically how spread apart ae the are
    # the last nth returns around their average. the return here being the close of the preious bar / the close of this bar.
    vol_20 = temp.groupby('date')['log_ret'].transform(lambda s: roll_std(s.shift(1), 20))
    vol_60 = temp.groupby('date')['log_ret'].transform(lambda s: roll_std(s.shift(1), 60))
    vol_90 = temp.groupby('date')['log_ret'].transform(lambda s: roll_std(s.shift(1), 90))

    # Sums per day only 
    sum_5  = temp.groupby('date')['log_ret'].transform(lambda s: roll_sum(s.shift(1), 5))
    sum_20 = temp.groupby('date')['log_ret'].transform(lambda s: roll_sum(s.shift(1), 20))
    sum_60 = temp.groupby('date')['log_ret'].transform(lambda s: roll_sum(s.shift(1), 60))
    sum_90 = temp.groupby('date')['log_ret'].transform(lambda s: roll_sum(s.shift(1), 90))
    
    # Create a new DataFrame to hold just our shiny new features, it includes only our first column of data which is our timestamps 
    features = pd.DataFrame({"timestamp": temp["timestamp"]})
    features ['EWMA'] = EWMA
    features ['vol_20'] = vol_20
    features ['vol_60'] = vol_60
    features ['vol_90'] = vol_90
    features['r_1n']  = temp['log_ret'] / (vol_20 + epsilon)
    features['r_5n']  = sum_5  / (vol_20 + epsilon)
    features['r_20n'] = sum_20 / (vol_20 + epsilon)

    features['r_60n'] = sum_60 / (vol_60 + epsilon)
    features['r_90n'] = sum_90 / (vol_90 + epsilon)


    # use below for debugging
    #print(f"checking out the data nd see if it behaved as we want")
    #print(features.head(21))
    
    # Here we can change the nans to 0 as it would be considered the average of the returns and also
    # when the market opens (our best window) the r_vol 90 and 60 don't really matter that much because we are looking at the micro and
    # not the macro
    # Fill the empty startup periods with 0 (Neutral)
    features.fillna(0.0, inplace=True)
    # Use below for debugging
    #print("checking again to see if the NA has been filled with 0s")
    #print (features.head(21))
    return features
