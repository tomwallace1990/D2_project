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

################# Functions #################
def missing_func(var):
	df1.loc[df1[var] == '.', var] = np.NaN

################# Data managment #################
print('\n')

df1 = pd.read_json(path_or_buf='data_with_twitter_info.json', orient ='index') # Read in

for value in ['Company number', 'Financial_year_ending', 'How the charity works', 'Trustees', 'Staff', 'Survived', 'Updated_expenditure', 'Volunteers', 'Website', \
 'What the charity does', 'Who the charity helps', 'updated_income']:
	df1.drop(columns=[value], inplace=True) # This line would drop unneeded columns if we wanted to at this stage - for now will pass the whole file out

for missingvar in ['Twitter Handle', 'Number of tweets in total', 'Twitter followers', 'Twitter following']:
	missing_func(missingvar)

df1 = df1[['Twitter Handle', 'Number of tweets in total', 'Twitter followers', 'Twitter following']]

print(df1)

print(list(df1))
print(df1.shape)

df1.to_json(path_or_buf='twitter_data_cleaned.json', orient='index') # Save the dataframe out to a JSON in the format 'index' which is easy to read and verify manually
#df1.to_csv(path_or_buf='temp1.csv')

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 