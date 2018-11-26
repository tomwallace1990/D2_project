#Analysis for Research question 4
#Written by Natalie Polack on 13th November 2018
#ITNBD2 Assignment
#This script reads the final analysis JSON file and does the analysis for Q4

import pandas as pd
import json
import datetime
#import numpy as np
import statsmodels.api as sm
#import scipy as sc

print("")

print(("This run was started at: "),datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

print("")

df1 = pd.read_json("Final_analysis_file.json", orient='index')

print("List of column headings:", list(df1))
print("")
print("List of data types in columns:", df1.dtypes)
print("")

#https://chartio.com/resources/tutorials/how-to-check-if-any-value-is-nan-in-a-pandas-dataframe/
print("Number of NaN:", df1.isnull().sum())
print("")

#https://stackoverflow.com/questions/50165953/python-dataframes-describing-a-single-column/50274029
print(df1['Staff'].describe())
print("")
print(df1['Income2018'].describe())
print("")
print(df1['Twitter following'].describe())
print("")

#https://stackoverflow.com/questions/42579908/use-corr-to-get-the-correlation-between-two-columns
print(('Correlation between Staff and Twitter following:'),df1['Staff'].corr(df1['Twitter following']))
print(('Correlation between Income2018 and Twitter following:'),df1['Income2018'].corr(df1['Twitter following']))
print("")

#https://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-in-certain-columns-is-nan
df2 = df1.dropna(subset = ['Staff', 'Income2018', 'Twitter following'])
print("Number of NaN:", df2.isnull().sum())
print("")

#https://datatofish.com/statsmodels-linear-regression/
#https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
#Linear regression using Staff to predict Twitter following
X = df2['Staff']
Y = df2['Twitter following']
X = sm.add_constant(X) #Adding a constant
model = sm.OLS(Y, X).fit()
predictions = model.predict(X)
#print_model = model.summary()
print(model.summary())
print("")

#Linear regression using Staff to predict Twitter following, with Income2018 as a control
X = df2[['Staff','Income2018']]
Y = df2['Twitter following']
X = sm.add_constant(X) #Adding a constant
model = sm.OLS(Y, X).fit()
predictions = model.predict(X)
print(model.summary())

print(("Run finished at: "),datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

exit()
