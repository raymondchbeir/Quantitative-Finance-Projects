#general libraries used 
import pandas as pd
import numpy as np
from src.features.volatility import roll_std
##################################################################
####                                                          ####
####                        1.3 + 1.4                         ####
####                  Candle Microstructure                   ####
####                         1.4 ip                          ####
##################################################################

def Candle_micro(df):
    temp = df.copy()
    #sorting by timestamp to make sure we have everything good 
    temp = temp.sort_values("timestamp").reset_index(drop=True)

    # Same block as before
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
    #getting the log return
    temp['log_ret'] = temp.groupby('date')['close'].transform(lambda s: np.log(s / s.shift(1))).fillna(0.0)
    # using vol20 to normalize
    vol_20 = temp.groupby('date')['log_ret'].transform(lambda s: roll_std(s.shift(1), 20))
    # creating the features column to make it start with the timestamp as a column so we can load days and not just count shit 
    features = pd.DataFrame({"timestamp": temp["timestamp"]})
    grouped = temp.groupby('date')
    ## Calculating the things normalized
    expected_move = temp['close'] * vol_20

    # Here we don't need groupby because we are only using each bar's information.
    features['hl_range'] =(temp['high'] - temp['low']) / (expected_move + epsilon)
    features['candle_body'] = (abs(temp['close'] - temp['open'])) / (expected_move + epsilon)
    features ['impulse_ratio'] = (temp['close'] - temp['open']) / ( temp['high'] - temp['low'] + epsilon)
    features ['up_wick_ratio'] = (temp['high'] - np.maximum(temp['close'],  temp['open'])) / ( temp['high'] - temp['low'] + epsilon)
    features ['low_wick_ratio'] = (np.minimum(temp['close'],  temp['open']) - temp['low']) / ( temp['high'] - temp['low'] + epsilon)
    features['wick_skew'] = features['up_wick_ratio'] - features['low_wick_ratio']


    # Fill the empty startup periods with 0 (Neutral)
    features.fillna(0.0, inplace=True)

    return features
