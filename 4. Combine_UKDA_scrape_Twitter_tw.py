#Combine data files
#Tom Wallace
#03/11/18
#This file merges the UKDA, Charity Commission, and TWitter into a single json file.

################################# Import packages #################################
import json
import pandas as pd
import datetime

################################# Main program #################################

starttime = datetime.datetime.now()
print(' ') 
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<')
print(' ')

df1 = pd.read_json(path_or_buf='UKDA_data_cleaned.json', orient ='index') # Read in the JSON file of the main data set as created in '1.1 CreatingSubsetofData_np.py' as a pandas data frame
df2 = pd.read_json(path_or_buf='new_scrape_data_cleaned.json', orient ='index') # Read in the JSON file of the new dara creared in '2.1. Wrangle_scrape_data_tw.py'
df3 = pd.read_json(path_or_buf='twitter_data_cleaned.json', orient ='index') # Read in the JSON file of the new dara creared in '3.1. Wrangle_twitter_data_tw.py'

df4 = pd.merge(df1, df2, left_index=True, right_index=True) # Merge df1 and df2 based on matching the index (charity numbers) which are uniquely identifying

df5 = pd.merge(df4, df3, left_index=True, right_index=True) # Merge df4 and df3 to create a combination of all 3

print(list(df5)) # Check the variables are all present
print(df5.shape) # Check the shape of the data is still correct

df5.to_json(path_or_buf='combined_data_file.json', orient='index') # Save the new comined dataframe out to a JSON

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 