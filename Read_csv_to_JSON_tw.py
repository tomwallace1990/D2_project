#Read CSV into JSON
#Tom Wallace
#21/09/18
#This file reads a CSV into a Pnadas dataframe, modifies it and saves it out to a JSON with the index format. It then reads it back in from JSON to a dataframe to test if the translation works.

################################# Import packages #################################
from urllib.request import urlopen as uReq
import csv
import requests
from time import sleep
import datetime
import random
import json
import pandas as pd
import numpy as np
import math as maths
import os.path

################################# Read in CSV and save as JSON #################################

now = datetime.datetime.now()
print(' ')
print('>>> Run initialized at ', now.strftime("%Y-%m-%d %H:%M") , ' <<<')
print(' ')

projectpath = './'

inputfilepath = projectpath + "CharityCharacteristics.csv" 

df = pd.DataFrame.from_csv(inputfilepath)

#print(df)

df.reset_index(inplace=True)
df.set_index(['ccnum', 'financial_year'], inplace=True)
df.drop(index='2006-07', level=1, inplace=True)
df.drop(index='2007-08', level=1, inplace=True)
df.drop(index='2008-09', level=1, inplace=True)
df.drop(index='2009-10', level=1, inplace=True)
df.drop(index='2010-11', level=1, inplace=True)
#df.drop(index='2011-12', level=1, inplace=True) # this is the row which is not being dropped
df.drop(index='2012-13', level=1, inplace=True)
df.drop(index='2013-14', level=1, inplace=True)
df.reset_index(inplace=True)
df.set_index(['ccnum'], inplace=True)

#print(df)

#df.drop(columns=['account_type'], inplace=True)

df.to_json(path_or_buf='active_data_file.json', orient='index')

df1 = pd.read_json(path_or_buf='active_data_file.json', orient ='index')

print(df1)

print('>>> Finished run at' , now.strftime("%H:%M:%S"),'<<<')