#Read CSV into JSON
#Tom Wallace
#Finished 21/09/18, annotations updated 26/09/18
#This file reads a CSV into a Pnadas dataframe, modifies it and saves it out to a JSON with the index format. It then reads it back in from JSON to a dataframe to test if the translation works.

################################# Import packages #################################
import csv # reads CSV
import json # Handles JSON
import pandas as pd # Managed the data while it's in memory and converts between CSV and JSON
import os.path

################################# Read in CSV and save as JSON #################################

now = datetime.datetime.now() # Get the current date/time to display to the user
print(' ') # White space used to increase readability of output window
print('>>> Run started at ', now.strftime("%Y-%m-%d %H:%M") , ' <<<') # Print start time - serves as a header for the output window
print(' ')

projectpath = './' # Hold the current folder (where the .py file resides) in a variable as the project path

inputfilepath = projectpath + "CharityCharacteristics.csv" # Grab the filepath of the CSV to be imported

df = pd.DataFrame.from_csv(inputfilepath) # Create a panda's dataframe from the CSV

#print(df) # Commented out prints used to check import has completed correctly

df.reset_index(inplace=True) # Remove the index of the frame which is asigned to column 0 on import (can be changed on import but we want a 2 level index)
df.set_index(['ccnum', 'financial_year'], inplace=True) # Set the 2 level index. The data is longitudinal so charity number (ccnum) and period (financial_year) uniquiely identify each case

df.drop(index='2006-07', level=1, inplace=True) # Drop periods not to be used in analysis - we want a cross section
df.drop(index='2007-08', level=1, inplace=True)
df.drop(index='2008-09', level=1, inplace=True)
df.drop(index='2009-10', level=1, inplace=True)
df.drop(index='2010-11', level=1, inplace=True)
#df.drop(index='2011-12', level=1, inplace=True) # this is the period which is going to be analysed. This could esily be changed by commenting out different lines
df.drop(index='2012-13', level=1, inplace=True)
df.drop(index='2013-14', level=1, inplace=True)

df.reset_index(inplace=True) # 2 level index no longer needed
df.set_index(['ccnum'], inplace=True) # Set index to charity number which is uniquely identifying within 1 time period

#print(df)

#df.drop(columns=['account_type'], inplace=True) # This line would drop unneeded columns if we wanted to at this stage - for now will pass the whole file out

df.to_json(path_or_buf='active_data_file.json', orient='index') # Save the dataframe out to a JSON in the format 'index' which is easy to read and verify manually

df1 = pd.read_json(path_or_buf='active_data_file.json', orient ='index') # Check the JSON reads back into a data frame 

print(df1) # Print the frame to check nothing has been lost

print('>>> Finished run at' , now.strftime("%H:%M:%S"),'<<<') # Footer the program with a finish time