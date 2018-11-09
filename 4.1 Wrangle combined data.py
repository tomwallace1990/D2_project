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
from scipy import stats
from scipy.stats import zscore


################################# Functions #################################

#checks for outliers using iqr and returns a dataset with those outliers converted to NaN
def iqrOutliers(dataSet, theString):
    newDataSet = dataSet.copy()
    calcSeries = newDataSet[theString]
    calcSeries = calcSeries.dropna()
    q1 = (np.percentile(calcSeries, 25))
    q3 = (np.percentile(calcSeries, 75))
    iqr = q3-q1
    minVal = q1 - (1.5 * iqr)
    maxVal = q3 + (1.5 * iqr)
    newDataSet.loc[((newDataSet[theString] > maxVal)|(newDataSet[theString] < minVal)), theString] = np.NaN
    return newDataSet


#checks for outliers using zScore (standard deviation basically) and returns a dataset with those outliers converted to NaN
def zScores(dataSet, theString):
	newDataSet = dataSet.copy()
	#print(newDataSet[theString])
	calcSeries = newDataSet[theString]
	calcSeries = calcSeries.dropna()
	theScores = (calcSeries - calcSeries.mean())/calcSeries.std(ddof=0)
	theScores.rename('Zscore', inplace=True)
	theScoresframe = theScores.to_frame()
	newDataSet = pd.merge(newDataSet, theScoresframe, left_index=True, right_index=True, how='outer')
	newDataSet.loc[((newDataSet['Zscore'] > 3)|(newDataSet['Zscore'] < -3)), theString] = np.NaN
	newDataSet.drop(columns=['Zscore'], inplace=True)
	return newDataSet

################################# Main program #################################

starttime = datetime.datetime.now() # Grab the date and time
print(' ') # Whitespace used to make the output window more readable
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<') # Header of the output, with the start time
print(' ')

df1 = pd.read_json(path_or_buf='combined_data_file.json', orient ='index') # Read in


###New variables
df1['Abs_funding_growth'] = df1['Income2018'] - df1['Income2011-2012']
describe = df1[['Abs_funding_growth']].describe()
#print(describe)

df1['Ratio_funding_growth'] = df1['Income2018'] / df1['Income2011-2012']
describe = df1[['Ratio_funding_growth']].describe()

###Outlier dropping
print(list(df1))

#'Government_funding' excluded for being too small - drops all data
outlierdroplist = ['Number of tweets in total', 'Twitter followers', 'Twitter following', 'Income2011-2012', 'Income2018', 'Funds_general_public', 'Prop_general_public_funding', 'Staff', 'Abs_funding_growth', 'Ratio_funding_growth']

df2=df1

for variable in outlierdroplist:
	print(variable)
	df2 = iqrOutliers(df2, variable)
	print(df1[variable].isna().sum(), df2[variable].isna().sum(), '- More than 0 outliers dropped:', df1[variable].isna().sum() < df2[variable].isna().sum(), '\n')

df2.to_json(path_or_buf='combined_data_file_cleaned.json', orient='index') # Save the dataframe out to a JSON in the format 'index' which is easy to read and verify manually
#df1.to_csv(path_or_buf='temp1.csv')
#df2.to_csv(path_or_buf='temp2.csv')

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 