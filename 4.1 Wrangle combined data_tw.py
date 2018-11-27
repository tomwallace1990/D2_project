#Wrangle combined data
#Tom Wallace
#5/11/18
#This file applies the final data management  to the combined data set created in '4. Combine_UKDA_scrape_Twitter_tw.py'. This involves generating two growth variables (which use data from different parts of the combined file) and dealing with outliers

################################# Import packages #################################
import datetime
import json
import pandas as pd
import numpy as np

################################# Functions #################################

def iqrOutliers(dataSet, theString): #checks for outliers using iqr and returns a dataset with those outliers converted to NaN
    newDataSet = dataSet.copy()
    calcSeries = newDataSet[theString] # To avoid missing data biasing the calculation of the percentiles, a series is created seperate from the main data and NaNs are then dropped for the calculation
    calcSeries = calcSeries.dropna()
    q1 = (np.percentile(calcSeries, 25))
    q3 = (np.percentile(calcSeries, 75))
    iqr = q3-q1
    minVal = q1 - (1.5 * iqr)
    maxVal = q3 + (1.5 * iqr)
    newDataSet.loc[((newDataSet[theString] > maxVal)|(newDataSet[theString] < minVal)), theString] = np.NaN
    return newDataSet

def zScores(dataSet, theString): #checks for outliers using zScore (standard deviation) and returns a dataset with those outliers converted to NaN
	newDataSet = dataSet.copy()
	calcSeries = newDataSet[theString]
	calcSeries = calcSeries.dropna()
	theScores = (calcSeries - calcSeries.mean())/calcSeries.std(ddof=0)
	theScores.rename('Zscore', inplace=True)
	theScoresframe = theScores.to_frame()
	newDataSet = pd.merge(newDataSet, theScoresframe, left_index=True, right_index=True, how='outer') # Because the zscores were calculated on a series with NaNs dropped they need to be remerged into the full dataset for the next step
	newDataSet.loc[((newDataSet['Zscore'] > 3)|(newDataSet['Zscore'] < -3)), theString] = np.NaN
	newDataSet.drop(columns=['Zscore'], inplace=True)
	return newDataSet

################################# Main program #################################

starttime = datetime.datetime.now()
print(' ')
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<')
print(' ')

df1 = pd.read_json(path_or_buf='combined_data_file.json', orient ='index') # Read in combined data constructed in '4. Combine_UKDA_scrape_Twitter_tw.py'

##### Growth variables #####
df1['Abs_funding_growth'] = df1['Income2018'] - df1['Income2011-2012']

df1['Ratio_funding_growth'] = df1['Income2018'] / df1['Income2011-2012']

##### Outlier dropping #####
#'Government_funding' excluded for being too small and skewed - drops all data!
outlierdroplist = ['Number of tweets in total', 'Twitter followers', 'Twitter following', 'Income2011-2012', 'Income2018', 'Funds_general_public', 'Prop_general_public_funding', 'Staff', 'Abs_funding_growth', 'Ratio_funding_growth']

df2=df1

for variable in outlierdroplist:
	print(variable)
	df2 = iqrOutliers(df2, variable)
	print(df1[variable].isna().sum(), df2[variable].isna().sum(), '- More than 0 outliers dropped:', df1[variable].isna().sum() < df2[variable].isna().sum(), '\n') # Print info to the screen about outliers dropped

##### Saving #####
df2.to_json(path_or_buf='Final_analysis_file.json', orient='index') # Save the dataframe to a final file used in all subsequent analysis

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 