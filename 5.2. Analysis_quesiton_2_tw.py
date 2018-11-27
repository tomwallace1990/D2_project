#Question 2 analysis
#Tom Wallace
#10/11/18
#This file performs statiscal analyiss on the data created by '4.1 Wrangle combined data_tw.py'. It seeks to asnwer the question 'Are charities which seek to help the public more popular on Twitter?'

################################# Import packages #################################
import datetime
import json
import numpy as np
import pandas as pd
import math as maths
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.api as sm

################################# Fucntions #################################

def linearreg(xlist, y): # This fuctnion applies an OLS regression with given X and Y varaibles
	df2 = df1.dropna(subset=xlist)
	df2 = df2.dropna(subset=[y])

	X = df2[xlist]
	X = sm.add_constant(X)
	y = df2[y]
	model = sm.OLS(y, X).fit()
	return(model)


def logit(xlist, y): # This fuctnion applies a logit regression with given X and Y varaibles
	df2 = df1.dropna(subset=xlist)
	df2 = df2.dropna(subset=[y])

	X = df2[xlist]
	X = sm.add_constant(X)
	y = df2[y]
	model_log = sm.Logit(y, X).fit()
	return(model_log)


################################# Main program #################################

starttime = datetime.datetime.now() 
print(' ') 
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<')
print(' ')

df1 = pd.read_json(path_or_buf='Final_analysis_file.json', orient ='index') 


df1 = df1[['Income2011-2012', 'Income2018', 'Abs_funding_growth', 'Ratio_funding_growth', 'Survived', 'Staff','Funds_general_public', 'Prop_general_public_funding', 'Government_funding', \
 'Prop_government_funding', 'Helps: The general public or mankind', 'Twitter Handle', 'Number of tweets in total', 'Twitter followers', 'Twitter following']] # Order the variables in a sensiable way
print(list(df1))
print(df1.shape)

df2 = df1.drop(df1.loc[df1['Helps: The general public or mankind']==1].index) # Create subsets of data based on the helps the public variable
df3 = df1.drop(df1.loc[df1['Helps: The general public or mankind']==0].index)

################################# Question 1 #################################
### Univariate
# Helps table
helps_table = df1['Helps: The general public or mankind'].value_counts()
print(helps_table)

# Describe
# Doesn't help public
describe = df2[['Income2018', 'Prop_general_public_funding']].describe()
print(describe)
describe = df2[['Twitter followers']].describe()
print(describe)

# Helps public
describe = df3[['Income2018', 'Prop_general_public_funding']].describe()
print(describe)
describe = df3[['Twitter followers']].describe()
print(describe)

# Histogram - outlier heavy
hist1 = df1['Twitter followers'].plot.hist(bins=100)
plt.show() # most charities don't revive most funding from public

### Modelling
# Linear
model = linearreg(['Helps: The general public or mankind', 'Income2018'], 'Twitter followers') # Independent/predictors in list, depenedent on its own at the end
print(model.summary())

# Logit
model_log = logit(['Twitter followers', 'Income2018'], 'Helps: The general public or mankind')
print(model_log.summary2())

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 