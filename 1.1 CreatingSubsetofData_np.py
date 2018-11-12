#Data Management
#Written by Natalie Polack on 7th November 2018
#ITNBD2 Assignment
#This script reads the JSON file, combines and renames columns and creates a new smaller dataframe 

import pandas as pd
import json
import datetime

print("")

print(("This run was started at: "),datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

print("")

df1 = pd.read_json("charity_oneyear.json", orient='index')

#1. Combine (add) the following ig variables into ‘government funding’: ig100, ig110, ig121, ig125, ig161, ig162, ig163, ig180
#https://kaijento.github.io/2017/04/22/pandas-create-new-column-sum/
df1['Government_funding'] = df1.ig100 + df1.ig110 + df1.ig121 + df1.ig125 + df1.ig161 + df1.ig162 + df1.ig163 + df1.ig180

#2. Create government funding proportion variable (for each charity gov income/total income which is itotal)
df1['Prop_government_funding'] = df1.Government_funding / df1.itotal

#3. Geneal public funding
df1['Prop_general_public_funding'] = df1.ig600 / df1.itotal

df1.rename(columns = {'ig600':'Funds_general_public'}, inplace = True)

#4. Rename itotal – ‘income_2011_12’
#http://cmdlinetips.com/2018/03/how-to-change-column-names-and-row-indexes-in-pandas/
df1.rename(columns={'itotal':'Income2011-2012'}, inplace=True)

#5. Select 5 columns to be kept: ccnum, government_funding, government_funding_proportion, non_government_funding, income_2011_12)
#https://stackoverflow.com/questions/34682828/extracting-specific-selected-columns-to-new-dataframe-as-a-copy
df2 = df1.filter(['Government_funding','Prop_government_funding','Funds_general_public', 'Prop_general_public_funding', 'Income2011-2012'], axis=1)

#6. Print list of column headings, data type in each column and check for NaN
#https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers
#https://stackoverflow.com/questions/29530232/how-to-check-if-any-value-is-nan-in-a-pandas-dataframe
print("List of column headings:", list(df2))
print("")
print("List of data types in columns:", df2.dtypes)
print("")
print("Number of NaN:", df2.isnull().sum().sum())
print("")

#7. Save the new dataframe with new name 
df2.to_json("UKDA_data_cleaned.json", orient='index')

#8. Print new dataframe to check it has worked
df3 = pd.read_json("UKDA_data_cleaned.json", orient='index')

print(df3)

#Sum columns to check Gov funding prop column is correct?

print("")

print(("Run finished at: "),datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

exit()