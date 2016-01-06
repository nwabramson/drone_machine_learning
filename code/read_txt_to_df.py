import os
import pandas as pd
from os.path import isfile, join
#import matplotlib.pyplot as plt
import re


def read_txt_to_df(directory):
    '''
    input directory of files to add  to dataframe
    output dataframe
    '''
    
    mission = directory[:4]
    quality = directory[-1:]
    cwd =  os.getcwd()
    os.chdir("files/" + directory)
    datafiles = os.listdir(".")

    df = pd.DataFrame()

    if len(datafiles) > 0 :

        for datafile in datafiles:

            df1 = pd.read_csv(datafile)
            df =  pd.concat([df,df1])

    else:
        # no good data so stub in values for bad data

        os.chdir(cwd)
        file_name = "missions/" + str(mission) + "_" + str(quality) + ".log"
        line = open(file_name).next()
        date = line[:10]
        time = line[11:22]
        df = pd.DataFrame(columns=['date', 'time', 'mission', 'quality'])
        df.loc[0] = [date, time, mission, quality]

    os.chdir(cwd)

    df['date_time']= pd.to_datetime(df['date'] + ' ' + df['time'] )

    return df

def add_flight_duration(df1):
    '''
    input df to add or update durations column given a mission
    return df with updated duration from beginning of flight
    '''

    try:
        t0 = df1['date_time'].min().value
    except:
        df1['duration']=0
        return df1
        
    df1['duration'] = t0

    date_time_iloc = list(df1.columns).index('date_time')
    duration_iloc = list(df1.columns).index('duration')

    for i in xrange(df1.shape[0]):

        df1.iloc[i, duration_iloc] = df1.iloc[i, date_time_iloc].value - t0

    return df1

def clean_columns(df):
    '''
    input data frame with unecessary columns
    output clean data frame
    '''

    cols = [ str(c) for c in df.columns if c.count(".") == 0]
    cols = [ str(c) for c in cols if c if not re.match("TERRAIN_DATA_-", c) ]
    cols = [ str(c) for c in cols if c if not re.match("TERRAIN_DATA_[0-9]+", c) ]
    cols = [ str(c) for c in cols if c if not re.match("AUTOPILOT_VERSION_", c) ]
    
    try:
        cols.remove('NAMED_VALUE_INT_name')
        return df[cols]
    except:
        return df[cols]

def show_timeseries(dfm1, dfm2, dfm3, dfm4, dfm5, cols, num_rows=4):
    start_col = 0
    total = num_rows**2
    i=0
    for i in xrange(len(cols)):
        if i%total == 0 and i != 0:
            cols_x = cols[start_col:i]
            start_col = i
            print cols_x, i
            for variable, num in zip(cols_x, xrange(total)):
                frame1 = plt.gca()
                frame1.xaxis.set_ticklabels([])
                plt.subplot(num_rows, num_rows, num+1)    
                plt.scatter(dfm1['duration']/1000, dfm1[variable], c='b')
                plt.scatter(dfm2['duration']/1000, dfm2[variable], c='r')
                plt.scatter(dfm3['duration']/1000, dfm3[variable], c='g')
                plt.scatter(dfm4['duration']/1000, dfm4[variable], c='y')
                plt.scatter(dfm5['duration']/1000, dfm5[variable], c='m')
                plt.ylabel(variable)
                #plt.xlim([0,100])

            plt.tight_layout()
            plt.show()

    cols_x = cols[start_col:i]
    print cols_x, i
    for variable, num in zip(cols_x, xrange(total)):
        frame1 = plt.gca()
        frame1.xaxis.set_ticklabels([])
        plt.subplot(num_rows, num_rows, num+1)    
        plt.scatter(dfm1['duration']/1000, dfm1[variable], c='b')
        plt.scatter(dfm2['duration']/1000, dfm2[variable], c='r')
        plt.scatter(dfm3['duration']/1000, dfm3[variable], c='g')
        plt.scatter(dfm4['duration']/1000, dfm4[variable], c='y')
        plt.scatter(dfm5['duration']/1000, dfm5[variable], c='m')
        plt.ylabel(variable)
        #plt.xlim([0,100])

#    plt.gca().tight_layout()
    plt.tight_layout()
    plt.show()

def write_mission_csv(mission, quality):

    dir_name = str(mission)+"_" +str(quality)
    df1 = pd.DataFrame()
    df1 = read_txt_to_df(dir_name)
    df1 = add_flight_duration(df1)
    df1 = clean_columns(df1)
    df1.to_csv("data/"+dir_name+".csv")

    return

def show_timeseries2(dfm1, dfm2, cols, num_rows=4):
    start_col = 0
    total = num_rows**2
    i=0
    for i in xrange(len(cols)):
        if i%total == 0 and i != 0:
            cols_x = cols[start_col:i]
            start_col = i
            print cols_x, i
            for variable, num in zip(cols_x, xrange(total)):
                frame1 = plt.gca()
                frame1.xaxis.set_ticklabels([])
                plt.subplot(num_rows, num_rows, num+1)    
                plt.scatter(dfm1['duration']/1000, dfm1[variable], c='b')
                plt.scatter(dfm2['duration']/1000, dfm2[variable], c='r')
                plt.ylabel(variable)
                #plt.xlim([0,100])

            plt.tight_layout()
            plt.show()

    cols_x = cols[start_col:i]
    print cols_x, i
    for variable, num in zip(cols_x, xrange(total)):
        frame1 = plt.gca()
        frame1.xaxis.set_ticklabels([])
        plt.subplot(num_rows, num_rows, num+1)    
        plt.scatter(dfm1['duration']/1000, dfm1[variable], c='b')
        plt.scatter(dfm2['duration']/1000, dfm2[variable], c='r')
        plt.ylabel(variable)
        #plt.xlim([0,100])

#    plt.gca().tight_layout()
    plt.tight_layout()
    plt.show()

