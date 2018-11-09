#Combine old and new data
#Tom Wallace
#24/09/18
#This file reads in the JSON created in 'Read_csv_to_JSON_tw.py' as a pandas dataframe and then reads in the scraped data created by 'Scrape_updated_data.py' and merges the two frames based on their uniquely itentifying charity numbers 

################################# Import packages #################################
import json
import pandas as pd
import os.path
import time
import datetime

################################# Main program #################################

starttime = datetime.datetime.now() # Grab the date and time
print(' ') # Whitespace used to make the output window more readable
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<') # Header of the output, with the start time
print(' ')

df1 = pd.read_json(path_or_buf='UKDA_data_cleaned.json', orient ='index') # Read in the JSON file of the main data set as created in 'Read_csv_to_JSON_tw.py' as a pandas data frame
#print(df1)
df2 = pd.read_json(path_or_buf='new_scrape_data_cleaned.json', orient ='index') # Read in the JSON file of the new dara creared in 'Scrape_updated_data.py'
#print(df2)
df3 = pd.read_json(path_or_buf='twitter_data_cleaned.json', orient ='index') # Read in the JSON file of the new dara creared in 'Scrape_updated_data.py'
#print(df3)


df4 = pd.merge(df1, df2, left_index=True, right_index=True) # Merge the new data frame with the origional based on matching the index (charity numbers) which are uniquely identifying
#print(df4)

df5 = pd.merge(df4, df3, left_index=True, right_index=True) # Merge the new data frame with the origional based on matching the index (charity numbers) which are uniquely identifying
#print(df4)

df5 = df5[['Income2011-2012', 'Income2018', 'Survived', 'Staff','Funds_general_public', 'Prop_general_public_funding', 'Government_funding', 'Prop_government_funding', 'Helps: The general public or mankind', \
 'Twitter Handle', 'Has Twitter', 'Number of tweets in total', 'Twitter followers', 'Twitter following']]

print(list(df5))
print(df5.shape)

df5.to_json(path_or_buf='combined_data_file.json', orient='index') # Save the new comined dataframe out to a JSON - commented out for now as this may be done ah-hoc during analysis
#df5.to_csv(path_or_buf='temp1.csv')

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 