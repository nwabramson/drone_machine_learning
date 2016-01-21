import numpy as np
import pandas as pd
import os
import cPickle as pickle
from profile import profile

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

if __name__ == '__main__':
    DOC = """
================================================================================
                Agribotix Mission Quality Estimation
================================================================================
    """
    print(DOC)

    datafile = "../data/" +  os.sys.argv[1] + ".csv"

    sign = pd.read_csv(datafile)

    with open("../data/agribotix_model.pkl") as f_un:
        model = pickle.load(f_un)

    with open("../data/cols.pkl") as f_un:
        events = pickle.load(f_un)

    df0 = pd.DataFrame(columns=events)
    s_mission = set(sign.columns)

    # find common model events in current mission 

    for i in ['_std', '_md', '_min', '_max', '_cnt']:
        event_base = [ e.replace(i,'') for e in events if e.endswith(i)]

    mission_events = list(set(event_base) & s_mission)

    s1 = profile(sign, mission_events, os.sys.argv[1])

    mission_events = list(set(events) & set(s1.columns))

    sign =  pd.concat([s1[mission_events],df0])

    agg_filename = "../data/" + os.sys.argv[1] + "_agg.csv"
    sign.to_csv(agg_filename)

    X = sign[events].fillna(-9999999.)
    X = X.values

    preds = np.clip(np.round(model.predict(X)), 1, 5)

    print
    print
    print preds
