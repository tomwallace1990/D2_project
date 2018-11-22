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

#BRING IN THE FILE
#bring in the final file ready for analysis
finalDataDF = pd.read_json('Final_analysis_file.json', orient='index')

##############################################
#HAS TWITTER ANALYSIS
##############################################

#creates the categorical column for proportion of general public funding which categorises into
#0=less than the mean
#1=equal to or greater than the mean
#only those charities that are funded by government or general public should be included in this analysis
finalDataDF['CatGeneralFunding'] = (finalDataDF['Funds_general_public']>0)
finalDataDF['CatGovtFunding'] = (finalDataDF['Government_funding']>0)
finalDataDF['Has Twitter'] = (finalDataDF['Has Twitter']==1)
dataSet2 = finalDataDF[finalDataDF['Has Twitter'].tolist()].copy()
dataSet3 = finalDataDF[finalDataDF['CatGeneralFunding'].tolist()].copy()

firstDataSet = dataSet2.append(dataSet3)
print(firstDataSet.shape)

####################################################

#UNIVARIATE ANALYSIS

#print summary statistics for each column
statsDF = firstDataSet[['Funds_general_public','Government_funding','Prop_government_funding','Prop_general_public_funding','Number of tweets in total']]
statsForAll = statsDF.describe()
statsForAll.to_csv('summaryStatistics2.csv')

##############################################

#makes a bar chart for has twitter
htBarChart = sns.countplot(x='Has Twitter', data=firstDataSet, palette='hls')
plt.title("Charities Who Have Twitter")
plt.xlabel('Has Twitter')
plt.ylabel("No of charities")
htBarChart.set(xticklabels=['No','Yes'])
htFig = htBarChart.get_figure()
htFig.savefig("hasTwitterBarChart2.png")
plt.close()

#makes a bar chart for governement funding
htBarChart = sns.countplot(x='CatGovtFunding', data=firstDataSet, palette='hls')
plt.title("Government Funding")
plt.xlabel('Government Funding')
plt.ylabel("No of charities")
htBarChart.set(xticklabels=['Not Received','Recieved'])
htFig = htBarChart.get_figure()
htFig.savefig("GovFundingBarChart2.png")
plt.close()

#makes a bar chart for has public funding
htBarChart = sns.countplot(x='CatGeneralFunding', data=firstDataSet, palette='hls')
plt.title("General Public Funding")
plt.xlabel('General Public Funding')
plt.ylabel("No of charities")
htBarChart.set(xticklabels=['Not Received','Recieved'])
htFig = htBarChart.get_figure()
htFig.savefig("PublicFundingBarChart2.png")
plt.close()

#makes a frequency table for has twitter
twitterFreq = pd.crosstab(firstDataSet['Has Twitter'], columns='count')
print(twitterFreq)

#makes a frequency table for Government funding
govtFreq = pd.crosstab(firstDataSet['CatGovtFunding'],columns='count')
print(govtFreq)

#makes a frequency table for General funding
publicFreq = pd.crosstab(firstDataSet['CatGeneralFunding'],columns='count')
print(publicFreq)


################################################

#BIVARIATE ANALYSIS

#Chi-square testing for has twitter on public funding
publicCrossTab = pd.crosstab(firstDataSet['CatGeneralFunding'],firstDataSet['Has Twitter'])
publicChisq = stats.chi2_contingency(publicCrossTab)
print(publicCrossTab)
print(publicChisq)

#Chi-square testing for has twitter on government funding
govtCrossTab = pd.crosstab(firstDataSet['CatGovtFunding'],firstDataSet['Has Twitter'])
govtChisq = stats.chi2_contingency(govtCrossTab)
print(govtCrossTab)
print(govtChisq)

#########################################################

#MULTIVARIATE ANALYSIS
#create logistic regression model on relevant variables, staff put in as a control for size
dataSet = firstDataSet[['Has Twitter','Prop_government_funding','Prop_general_public_funding', 'Income2018']].copy()
dataSet.dropna(axis = 0, how='any', inplace=True)
y = dataSet['Has Twitter']
dataSet1 = dataSet.drop(columns = ['Has Twitter'])
dataSet1 = sm.add_constant(dataSet1)
logModel1 = sm.Logit(y, dataSet1).fit()
print(logModel1.summary2())

###################################################
#NUMBER OF TWEETS ANALYSIS
###################################################

#UNIVARIATE ANALYSIS
#only those charities who have government funding or general public funding AND have a twitter handle should be included
secondDataSet = firstDataSet[firstDataSet['Has Twitter'].tolist()].copy()

#create a histogram of number of tweets
#Have to drop NaNs for the histogram
tweets=secondDataSet['Number of tweets in total'].copy().dropna().tolist()
tweetsHist = sns.distplot(tweets)
plt.title("Number of tweets per charity")
plt.xlabel("Number")
plt.ylabel("Frequency")
tweetfig = tweetsHist.get_figure()
tweetfig.savefig("NumberOfTweetsHistogram.png")
plt.close()

#create histogram of proportion of government funding amongst those who receive it
dataSet1 = secondDataSet[secondDataSet['CatGovtFunding'].tolist()]
govtInc=dataSet1['Prop_government_funding'].copy().dropna().tolist()
govFigHist = sns.distplot(govtInc)
plt.title("Government Funding Proportion")
plt.xlabel("Proportion of funding")
plt.ylabel("Frequency")
govtfig = govFigHist.get_figure()
govtfig.savefig("GovernmentFundingHistogram.png")
plt.close()

#shows histogram of proportion of public funding amongst those who receive it
dataSet2 = secondDataSet[secondDataSet['CatGeneralFunding'].tolist()]
publicInc=dataSet2['Prop_general_public_funding'].copy().dropna().tolist()
pubFigHist = sns.distplot(publicInc)
plt.title("Public Funding")
plt.xlabel("Proportion of general public funding")
plt.ylabel("Frequency")
publicfig = pubFigHist.get_figure()
publicfig.savefig("PublicFundingHistogram.png")
plt.close()


#####################################################

#BIVARIATE ANALYSIS

# make a correlation matrix using seaborn 
# not used in final report due to space restriction
corr = secondDataSet[['Prop_general_public_funding','Prop_government_funding','Number of tweets in total']].corr()
cmap = sns.diverging_palette(220, 10, as_cmap=True)
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
labels = ['PropGenFunding','PropGovtFunding','NoOfTweets']
sns.heatmap(corr, mask=mask,cmap=cmap, vmax=.3,linewidths=.5)
plt.rcParams["axes.labelsize"] = 6
plt.title('Diagonal correlation matrix for Final Data Set',fontsize=10)
ax = plt.gca()
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)
plt.tight_layout()
plt.show()
plt.close()

#gives the correlation figure instead
print(secondDataSet[['Prop_general_public_funding','Number of tweets in total']].corr(), ' is the public funding corr')
print(secondDataSet[['Prop_government_funding','Number of tweets in total']].corr(), ' is the govt funding corr')


##################################################

#MULTIVARIATE ANALYSIS

#linear regression for relevant variables, Staff put in as a control for size
linearDataSet = secondDataSet[['Number of tweets in total','Prop_government_funding','Prop_general_public_funding', 'Income2018']].copy()
linearDataSet.dropna(axis = 0, how='any',inplace=True)
Y = linearDataSet['Number of tweets in total']
linear1 = linearDataSet.drop(columns = ['Number of tweets in total'])
linear1 = sm.add_constant(linear1) # adding a constant
model1 = sm.OLS(Y, linear1).fit()
print(model1.summary())

