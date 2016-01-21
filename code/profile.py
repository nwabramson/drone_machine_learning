import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import os
import datetime
import forecastio
import re
from scipy import stats

def find_lat_lon(df):

    latitude = 0
    longitude = 0 

    # lat lon values may be initialized to 1 so look for non zero values and return

    l_lon = [s for s in df.columns if "_lon_min" in s and df[s].values != 0 ] + [ s for s in df.columns if "_lon_max" in s and df[s].values != 0 ]
    l_lon = [ float(df[s].values*10.**-7) for s in df[l_lon] if bool(pd.notnull(df[s].values))]

    l_lat = [s for s in df.columns if "_lat_min" in s and df[s].values != 0 ] + [ s for s in df.columns if "_lat_max" in s and df[s].values != 0 ]
    l_lat = [ float(df[s].values*10.**-7) for s in df[l_lat] if bool(pd.notnull(df[s].values))]

    if len(l_lon) > 0 :
        longitude = l_lon[0]
    if len(l_lat) > 0 :
        latitude = l_lat[0]
        
    return latitude, longitude
#    return df[latitude].value, df[longitude].value


def weather_data(lat, lng, date_time):

    df_ll = pd.DataFrame(columns = ['latitude', 'longitude'])
    df_ll.loc[0] = [lat, lng]
    api_key = '35011de208e868f1429f12f125baf8ea'

     #date = datetime.datetime(2015, 12, 20, 3, 31, 59)
    try:
        date = pd.to_datetime(date_time).to_datetime()
        forecast = forecastio.load_forecast(api_key, lat, lng, time=date, units="us")
        hourly = forecast.hourly()
        d = hourly.data[0].d
        df = pd.DataFrame(columns = [str(c) for c in d.keys()])
        df.loc[0] = [c for c in d.values()]
        df = pd.concat([df_ll, df], axis = 1 )
        return  df
    except:
        return df_ll

def log_data(file_name):
    ''' return data from log counts
    '''
    file_name = "../missions/" + file_name + ".log"
    log_rows = sum(1 for line in open(file_name))
    bad_rows = sum(1 for line in open(file_name) if 'BAD' in line )

    try:
        line = os.popen( "grep 'lat :' '{}' | head -1".format(file_name) ).read()
        date_time = line[:22]

    except:
        date_time = '1970-01-01 00:00:00.00'

    return bad_rows, log_rows, date_time 

def profile(df, events, filename):

    final_cols = ['duration', 'bad_count', 'log_rows', 'date_time']

    for c in events:
        final_cols.append(str(c) + "_md")
        final_cols.append(str(c) + "_std")
        final_cols.append(str(c) + "_min")
        final_cols.append(str(c) + "_max")
        final_cols.append(str(c) + "_cnt")

    sign_df = pd.DataFrame(columns=final_cols)

    sign_df_command = "sign_df.loc[0] = [duration, bad_count, log_rows, date_time "

    for e in events:
        sign_df_command = sign_df_command + ", df['"+ e+ "'].median(), df['"+e+"'].std(), df['"+e+"'].min(), df['"+e+"'].max(), df['"+e+"'].count()"

    sign_df_command = sign_df_command + "]"

    bad_count, log_rows, date_time = log_data(filename)
    duration = df.duration.max()

    exec(sign_df_command)

    latitude, longitude = find_lat_lon(sign_df)

    df_weather = weather_data(latitude, longitude, date_time)

    sign_df = pd.concat([sign_df, df_weather], axis = 1 )

    return sign_df
