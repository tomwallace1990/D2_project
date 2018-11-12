#Wrangle scrape data
#Tom Wallace
#10/10/18
#This file manages the data scraped from the Charity Commission website in file 2. This involves setting missing data, breaking the 'Who the charity helps' variable into binaries, renaming, and dropping variables which won't be used in the analysis.

################################# Import packages #################################
import datetime
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

################################# Main program #################################

starttime = datetime.datetime.now() # Grab the date and time
print(' ') # Whitespace used to make the output window more readable
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<') # Header of the output, with the start time
print(' ')

df4 = pd.read_json(path_or_buf='new_scrape_data.json', orient ='index') # Read in data from '2. Scrape_updated_data_tw.py'

##### Income #####
df4.rename(columns = {'updated_income':'Income2018'}, inplace = True) # Rename income
df4.loc[df4['Income2018'] == -99, 'Income2018'] = np.NaN # Set the missing marker used in the scrape '-99' to numpy NaN

##### Who the charity helps #####
df4.rename(columns = {'Who the charity helps':'helps'}, inplace = True) # Rename to 'helps'
df41 = df4.drop(df4.loc[df4['helps']=='.'].index) # Create a new dataframe excluding all those with missing data for 'helps'
mlb = MultiLabelBinarizer() # Store the binarizer in a variable
helpscolumn = df41['helps'] # Make the 'helps' column into a series
df5 = pd.DataFrame(mlb.fit_transform(helpscolumn),columns=mlb.classes_, index=df41.index) # Apply the binarizer to the series to create a new data frame with multiple binary columns for each category in the origional column

df6 = pd.merge(df4, df5, left_index=True, right_index=True, how='outer') # Merge the new binary columns back into the origional frame

##### Rename binary column #####
df6.rename(columns = {'The general public or mankind':'Helps: The general public or mankind'}, inplace = True) # This is the binary column which is going to be used in the analysis

##### Drops #####
for value in ['Company number', 'Financial_year_ending', 'How the charity works', 'Trustees', 'Updated_expenditure', 'Volunteers', 'Website', 'What the charity does', 'helps', \
 'Children or young people', 'Elderly or old people', 'Other charities or voluntary bodies', 'Other defined groups', 'People of a particular ethnic or racial origin', 'People with disabilities']:
	df6.drop(columns=[value], inplace=True) # Drop columns not needed in the analysis

##### Checking and saving #####
print(list(df6)) # Check the correct columns are present
print(df6.shape) # Check the shape of the data

df6.to_json(path_or_buf='new_scrape_data_cleaned.json', orient='index') # Save the managed data to a new json

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 