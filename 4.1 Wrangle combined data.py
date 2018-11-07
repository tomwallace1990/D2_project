#Analysis test
#Tom Wallace
#24/09/18
#This file 
################################# Import packages #################################
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import requests
from time import sleep
import time
import datetime
import random
import json
import pandas as pd
import numpy as np
import math as maths
import os.path
from sklearn.preprocessing import MultiLabelBinarizer

################################# Main program #################################

starttime = datetime.datetime.now() # Grab the date and time
print(' ') # Whitespace used to make the output window more readable
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<') # Header of the output, with the start time
print(' ')

df1 = pd.read_json(path_or_buf='combined_data_file.json', orient ='index') # Read in

df1['Abs_funding_growth'] = df1['Income2018'] - df1['Income2011-2012']
describe = df1[['Abs_funding_growth']].describe()
print(describe)

df1['Ratio_funding_growth'] = df1['Income2018'] / df1['Income2011-2012']
describe = df1[['Ratio_funding_growth']].describe()
print(describe)

print(list(df1))
print(df1.shape)

df1.to_json(path_or_buf='combined_data_file_cleaned.json', orient='index') # Save the dataframe out to a JSON in the format 'index' which is easy to read and verify manually
#df1.to_csv(path_or_buf='temp1.csv')

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 