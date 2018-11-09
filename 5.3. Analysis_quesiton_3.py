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
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.api as sm

################################# Fucntions #################################

def linearreg(xlist, y):
	df2 = df1.dropna(subset=xlist)
	df2 = df2.dropna(subset=[y])

	X = df2[xlist]
	X = sm.add_constant(X)
	y = df2[y]
	model = sm.OLS(y, X).fit()
	return(model)


def logit(xlist, y):
	df2 = df1.dropna(subset=xlist)
	df2 = df2.dropna(subset=[y])

	X = df2[xlist]
	X = sm.add_constant(X)
	y = df2[y]
	model_log = sm.Logit(y, X).fit()
	return(model_log)


################################# Main program #################################

starttime = datetime.datetime.now() # Grab the date and time
print(' ') # Whitespace used to make the output window more readable
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<') # Header of the output, with the start time
print(' ')

df1 = pd.read_json(path_or_buf='Final_analysis_file.json', orient ='index') # Read in


df1 = df1[['Income2011-2012', 'Income2018', 'Abs_funding_growth', 'Ratio_funding_growth', 'Survived', 'Staff','Funds_general_public', 'Prop_general_public_funding', 'Government_funding', \
 'Prop_government_funding', 'Helps: The general public or mankind', 'Twitter Handle', 'Number of tweets in total', 'Twitter followers', 'Twitter following']]
print(list(df1))
print(df1.shape)
#df1.to_csv(path_or_buf='temp1.csv')

df2 = df1.drop(df1.loc[df1['Helps: The general public or mankind']==0].index)

################################# Question 1 #################################
###Univariate
#Describe
describe = df1[['Income2018', 'Prop_general_public_funding', 'Twitter followers']].describe()
print(describe)

describe = df2[['Income2018', 'Prop_general_public_funding', 'Twitter followers']].describe()
print(describe)


#helps table
helps_table = df1['Helps: The general public or mankind'].value_counts()
print(helps_table)

#Histogram - outlier heavy
df3 = df1.drop(df1.loc[df1['Twitter followers']>=600000].index)
hist1 = df3['Twitter followers'].plot.hist(bins=100)
plt.show() # most charities don't revive most funding from public
"""
###Modelling
#Linear
model = linearreg(['', ''], '') # Independent/predictors in list, depenedent on its own at the end
print(model.summary())

#Logit
model_log = logit(['', ''], '') # Independent/predictors in list, depenedent on its own at the end
print(model_log.summary2()) # Negative effect of being government funded on survival
"""
finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 