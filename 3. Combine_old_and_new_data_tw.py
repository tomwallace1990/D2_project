#Combine old and new data
#Tom Wallace
#24/09/18
#This file reads in the JSON created in 'Read_csv_to_JSON_tw.py' as a pandas dataframe and then reads in the scraped data created by 'Scrape_updated_data.py' and merges the two frames based on their uniquely itentifying charity numbers 

################################# Import packages #################################
import json
import pandas as pd
import os.path

################################# Main program #################################

df1 = pd.read_json(path_or_buf='active_data_file.json', orient ='index') # Read in the JSON file of the main data set as created in 'Read_csv_to_JSON_tw.py' as a pandas data frame
print(df1)
df2 = pd.read_json(path_or_buf='new_scrape_data.json', orient ='index') # Read in the JSON file of the new dara creared in 'Scrape_updated_data.py'
print(df2)

df3 = pd.merge(df1, df2, left_index=True, right_index=True) # Merge the new data frame with the origional based on matching the index (charity numbers) which are uniquely identifying
print(df3)
#df3.to_json(path_or_buf='active_data_file_updated.json', orient='index') # Save the new comined dataframe out to a JSON - commented out for now as this may be done ah-hoc during analysis

#df3.to_csv(path_or_buf='active_data_file_updated_csv.csv')