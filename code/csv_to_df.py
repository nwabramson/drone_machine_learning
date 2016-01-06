import os
import pandas as pd
from os.path import isfile, join
from read_txt_to_df import read_txt_to_df, add_flight_duration, clean_columns, write_mission_csv, show_timeseries2
import re
import sys

write_mission_csv(sys.argv[1], sys.argv[2])
