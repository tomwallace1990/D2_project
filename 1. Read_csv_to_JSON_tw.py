#Read CSV into JSON
#Tom Wallace
#Finished 21/09/18, annotations updated 26/09/18
#This file reads a CSV into a Pnadas dataframe, modifies it and saves it out to a JSON with the index format. It then reads it back in from JSON to a dataframe to test if the translation works.

################################# Import packages #################################
import csv # reads CSV
import json # Handles JSON
import pandas as pd # Managed the data while it's in memory and converts between CSV and JSON
import os.path
import datetime

################################# Read in CSV and save as JSON #################################

now = datetime.datetime.now() # Get the current date/time to display to the user
print(' ') # White space used to increase readability of output window
print('>>> Run started at ', now.strftime("%Y-%m-%d %H:%M") , ' <<<') # Print start time - serves as a header for the output window
print(' ')

projectpath = './' # Hold the current folder (where the .py file resides) in a variable as the project path

datapath = 'Original data/' # Original data is held in another folder to make the git repo tider

inputfilepath = projectpath + datapath + "CharityCharacteristics.csv" # Grab the filepath of the CSV to be imported

df = pd.DataFrame.from_csv(inputfilepath) # Create a panda's dataframe from the CSV

df.reset_index(inplace=True) # Remove the index of the frame which is asigned to column 0 on import (can be changed on import but we want a 2 level index)
df.set_index(['ccnum', 'financial_year'], inplace=True) # Set the 2 level index. The data is longitudinal so charity number (ccnum) and period (financial_year) uniquiely identify each case

for year in ['06-07', '07-08', '08-09', '09-10', '10-11', '12-13', '13-14']: # Drop periods not to be used in analysis - we want a cross section. '2011-12' is left out as this is the period we want to keep.
	df.drop(index='20' + year, level=1, inplace=True) 

df.reset_index(inplace=True) # 2 level index no longer needed
df.set_index(['ccnum'], inplace=True) # Set index to charity number which is uniquely identifying within 1 time period

df.to_json(path_or_buf= projectpath + 'active_data_file.json', orient='index') # Save the dataframe out to a JSON in the format 'index' which is easy to read and verify manually

df1 = pd.read_json(path_or_buf= projectpath + 'active_data_file.json', orient ='index') # Check the JSON reads back into a data frame 

print(df1) # Print the frame to check nothing has been lost

print('>>> Finished run at' , now.strftime("%H:%M:%S"),'<<<') # Footer the program with a finish time