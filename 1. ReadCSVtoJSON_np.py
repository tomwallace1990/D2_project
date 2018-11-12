#ReadCSVtoJSON
#Written by Natalie Polack on 27th October 2018
#ITNBD2 Assignment
#This script reads a CSV file, imports it into a Pandas dataframe and saves in a JSON format

import csv
import pandas as pd
import json
import datetime
#import os.path Not sure how to use this module

#Print a blank line before and after the date and time
#https://stackoverflow.com/questions/13872049/print-empty-line
print("")

#These sites show how to get the current date and time 
#https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
#https://www.pythonforbeginners.com/basics/python-datetime-time-examples
#now = datetime.datetime.now()

print(("This run was started at: "),datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

print("")

projectpath = './' # Hold the current folder (where the .py file resides) in a variable as the project path

datapath = 'Original data/' # Original data is held in another folder to make the git repo tider

inputfilepath = projectpath + datapath + "CharityCharacteristics.csv" # Grab the filepath of the CSV to be imported

# Create a Pandas dataframe from the CSV file
#https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/
df = pd.read_csv(inputfilepath)

#Removes the index that has been automatically assigned to column A: aid
#inplace=True means the change is made on the same copy and doesn't have to be assigned back to df
#inplace=False means a new copy so would need to be assigned back to df
#https://github.com/pandas-dev/pandas/issues/16263
#https://stackoverflow.com/questions/43893457/python-pandas-understanding-inplace-true
#https://www.geeksforgeeks.org/python-pandas-dataframe-reset_index/
df.reset_index(inplace=True)

#Set the index with 2 levels using Charity Number 'ccnum' and Financial Year 'financial_year'
df.set_index(["ccnum", "financial_year"],inplace=True)

#Drop all financial years except '2011-12' as this is the year we are going to use
#In the index wt=ith 2 levels: ccnum is level 0 and financial_year is level 1
df.drop(["2006-07", "2007-08", "2008-09", "2009-10", "2010-11", "2012-13", "2013-14"], level=1, inplace=True) 

#Reset the index again after dropping the years that aren't needed
df.reset_index(inplace=True)

#Set the index using Charity Number 'ccnum'
df.set_index(["ccnum"],inplace=True)

#Show the first 10 rows to check dropping years and reseting the index has worked
#https://chrisalbon.com/python/data_wrangling/load_json_file_into_pandas/
print(df.head(10))

#save as JSON
#https://galaxydatatech.com/2017/12/10/saving-pandas-data/
#DataFrame.to_json(path_or_buf=None, orient=None, date_format=’epoch’, double_precision=10, force_ascii=True, date_unit=’ms’, default_handler=None)
#Use orient=index This reads a line at a time and uses row numbers and column headings to label the data

df.to_json("charity_oneyear.json", orient='index')

#Read the json file and print the dataframe to check it has worked
#https://www.quora.com/How-do-I-read-a-big-JSON-file-with-Python
df1 = pd.read_json("charity_oneyear.json", orient='index')
print(df1)

print("")

print(("Run finished at: "),datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

exit()