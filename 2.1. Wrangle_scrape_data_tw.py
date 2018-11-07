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

################# Data managment #################
print('\n')

df4 = pd.read_json(path_or_buf='new_scrape_data.json', orient ='index') # Read in

df4.rename(columns = {'updated_income':'Income2018'}, inplace = True)
print(df4['Income2018'])
df4.loc[df4['Income2018'] == -99, 'Income2018'] = np.NaN
print(df4['Income2018'])

df4.rename(columns = {'Who the charity helps':'helps'}, inplace = True)

df41 = df4.drop(df4.loc[df4['helps']=='.'].index)

mlb = MultiLabelBinarizer()

helpscolumn = df41['helps']

df5 = pd.DataFrame(mlb.fit_transform(helpscolumn),columns=mlb.classes_, index=df41.index)

df6 = pd.merge(df4, df5, left_index=True, right_index=True, how='outer') # Merge the new data frame with the origional based on matching the index (charity numbers) which are uniquely identifying

"""
for each in ['Children or young people', 'Elderly or old people', 'Other charities or voluntary bodies', 'Other defined groups', 'People of a particular ethnic or racial origin', 'People with disabilities', 'The general public or mankind']:
	tab = df6[each].value_counts()
	print(tab, '\n')
"""

df6.rename(columns = {'The general public or mankind':'Helps: The general public or mankind'}, inplace = True)

for value in ['Company number', 'Financial_year_ending', 'How the charity works', 'Trustees', 'Updated_expenditure', 'Volunteers', 'Website', 'What the charity does', 'helps', \
 'Children or young people', 'Elderly or old people', 'Other charities or voluntary bodies', 'Other defined groups', 'People of a particular ethnic or racial origin', 'People with disabilities']:
	df6.drop(columns=[value], inplace=True) # This line would drop unneeded columns if we wanted to at this stage - for now will pass the whole file out

df6 = df6[['Income2018', 'Survived', 'Staff', 'Helps: The general public or mankind']]

print(list(df6))
print(df6.shape)

df6.to_json(path_or_buf='new_scrape_data_cleaned.json', orient='index') # Save the dataframe out to a JSON in the format 'index' which is easy to read and verify manually
#df6.to_csv(path_or_buf='temp1.csv')

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 