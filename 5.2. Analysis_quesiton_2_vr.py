#Created by Vikki Richardson 5/11/18
#In relation to question 2 "How is source of funding related to charity use of Twitter?"
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats
from patsy import dmatrices, build_design_matrices
from matplotlib.ticker import *
import statsmodels.api as sm
import seaborn as sns
sns.set(style='white')
sns.set(style='whitegrid',color_codes=True)

#bring in the final file ready for analysis
finalDataDF = pd.read_json('Final_analysis_file.json', orient='index')

#print summary statistics for each column
statsForAll = finalDataDF.describe()
statsForAll.to_csv('summaryStatistics.csv')

print('**************************************')
print('Has Twitter info')

#creates the categorical column for proportion of general public funding which categorises into
#0=less than the mean
#1=equal to or greater than the mean
#this is for chi square testing for has twitter
finalDataDF['CatGeneralFunding'] = (finalDataDF['Funds_general_public']>0)
finalDataDF['CatGovtFunding'] = (finalDataDF['Government_funding']>0)
#makes a frequency table for has twitter
twitterFreq = pd.crosstab(finalDataDF['Has Twitter'], columns='count')
print(twitterFreq)
#makes a frequency table for Government funding
govtFreq = pd.crosstab(finalDataDF['CatGovtFunding'],columns='count')
print(govtFreq)
#makes a frequency table for General funding
publicFreq = pd.crosstab(finalDataDF['CatGeneralFunding'],columns='count')
print(publicFreq)

#Chi-square testing for has twitter on public funding
publicCrossTab = pd.crosstab(finalDataDF['CatGeneralFunding'],finalDataDF['Has Twitter'])
publicChisq = stats.chi2_contingency(publicCrossTab)#, axis=None, ddof=1)
print(publicCrossTab)
print(publicChisq)
print('is the public chisq')

#Chi-square testing for has twitter on government funding
govtCrossTab = pd.crosstab(finalDataDF['CatGovtFunding'],finalDataDF['Has Twitter'])
govtChisq = stats.chi2_contingency(govtCrossTab)#, axis=None, ddof=1)
print(govtCrossTab)
print(govtChisq)
print('is the govt chisq')

#makes a bar chart for has twitter
htBarChart = sns.countplot(x='Has Twitter', data=finalDataDF, palette='hls')
plt.title("Charities Who Have Twitter")
plt.xlabel('Has Twitter')
plt.ylabel("No of charities")
htBarChart.set(xticklabels=['No','Yes'])
htFig = htBarChart.get_figure()
htFig.savefig("hasTwitterBarChart.png")
plt.close()

#makes a bar chart for governement funding
htBarChart = sns.countplot(x='CatGovtFunding', data=finalDataDF, palette='hls')
plt.title("Government Funding")
plt.xlabel('Government Funding')
plt.ylabel("No of charities")
htBarChart.set(xticklabels=['Not Received','Recieved'])
htFig = htBarChart.get_figure()
htFig.savefig("GovFundingBarChart.png")
plt.close()

#makes a bar chart for has public funding
htBarChart = sns.countplot(x='CatGeneralFunding', data=finalDataDF, palette='hls')
plt.title("General Public Funding")
plt.xlabel('General Public Funding')
plt.ylabel("No of charities")
htBarChart.set(xticklabels=['Not Received','Recieved'])
htFig = htBarChart.get_figure()
htFig.savefig("PublicFundingBarChart.png")
plt.close()

#gives indication of things like mean of income for those that have twitter vs those that don't 
statsByTwitter = finalDataDF.groupby('Has Twitter').mean()
statsByTwitter.to_csv('MeanByHasTwitter.csv')

#create logistic regression model on relevant variables, staff put in as a control for size
dataSet = finalDataDF[['Has Twitter','Prop_government_funding','Prop_general_public_funding', 'Staff', 'Income2018']].copy()
dataSet.dropna(axis = 0, how='any', inplace=True)
y = dataSet['Has Twitter']
dataSet.drop(columns = ['Has Twitter'], inplace=True)
dataSet = sm.add_constant(dataSet)
logModel = sm.Logit(y, dataSet).fit()
print(logModel.summary2())

print('********************************************')
print('Number of tweets info')


#create a histogram of number of tweets
#Have to drop NaNs for the histogram
tweets=finalDataDF['Number of tweets in total'].copy().dropna().tolist()
tweetsHist = sns.distplot(tweets)
plt.title("Number of tweets per charity")
plt.xlabel("Number")
plt.ylabel("Frequency")
tweetfig = tweetsHist.get_figure()
tweetfig.savefig("NumberOfTweetsHistogram.png")
plt.close()

# make a correlation matrix using seaborn 
corr = finalDataDF[['Funds_general_public','Prop_general_public_funding','Government_funding','Prop_government_funding','Income2011-2012','Income2018','Number of tweets in total']].corr()
cmap = sns.diverging_palette(220, 10, as_cmap=True)
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
labels = ['PublicFunding','PropGenFunding','GovtFunding','PropGovtFunding','2011Income','2018Income','NoOfTweets']
sns.heatmap(corr, mask=mask,cmap=cmap, vmax=.3,linewidths=.5)
plt.rcParams["axes.labelsize"] = 6
plt.title('Diagonal correlation matrix for Final Data Set',fontsize=10)
ax = plt.gca()
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)
plt.tight_layout()
plt.show()
plt.close()

#linear regression for relevant variables, Staff put in as a control for size
linearDataSet = finalDataDF[['Number of tweets in total','Prop_government_funding','Prop_general_public_funding', 'Staff', 'Income2018']].copy()
linearDataSet.dropna(axis = 0, how='any', inplace=True)
Y = linearDataSet['Number of tweets in total']
linearDataSet.drop(columns = ['Number of tweets in total'], inplace=True)
X = linearDataSet
X = sm.add_constant(X) # adding a constant
model = sm.OLS(Y, X).fit()
print(model.summary())

