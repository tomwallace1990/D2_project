#Analysis test
#Tom Wallace
#24/09/18
#This file 
################################# Import packages #################################
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import requests
from time import sleep
import time
import datetime
import random
import json
import pandas as pd
import numpy as np
import math as maths
import os.path

################################# Main program #################################

starttime = datetime.datetime.now() # Grab the date and time
print(' ') # Whitespace used to make the output window more readable
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<') # Header of the output, with the start time
print(' ')

################# Data managment #################
print('\n')

df3 = pd.read_json(path_or_buf='active_data_file.json', orient ='index') # Read in

#print(list(df3))

describe = df3[['ig100', 'ig110', 'ig121', 'ig125', 'ig161', 'ig162', 'ig163', 'ig180']].describe()
#print(describe)
df3['Government_funding'] = df3['ig100'] + df3['ig110'] + df3['ig121'] + df3['ig125'] + df3['ig161'] + df3['ig162'] + df3['ig163'] + df3['ig180']
describe = df3[['Government_funding']].describe()
#print(describe)

df3['Prop_government_funding'] = df3['Government_funding'] / df3['itotal']
describe = df3[['Prop_government_funding']].describe()
#print(describe)

df3['Prop_general_public_funding'] = df3['ig600'] / df3['itotal']
describe = df3[['Prop_general_public_funding']].describe()
#print(describe)

df3['Nongovernment_funding'] = df3['ig600'] + df3['ig500'] + df3['ig300'] + df3['ig175'] + df3['ig140']
describe = df3[['Nongovernment_funding']].describe()
#print(describe)

df3['Prop_nongov_funding'] = df3['Nongovernment_funding'] / df3['itotal']
describe = df3[['Prop_nongov_funding']].describe()
#print(describe)

df3.rename(columns = {'ig600':'Funds_general_public'}, inplace = True)
df3.rename(columns = {'ig500':'Funds_nonprofit'}, inplace = True)
df3.rename(columns = {'ig300':'Funds_Business_sector'}, inplace = True)
df3.rename(columns = {'ig175':'Funds_universities'}, inplace = True)
df3.rename(columns = {'ig140':'Funds_NHS'}, inplace = True)

df3.rename(columns = {'itotal':'Income2011-2012'}, inplace = True)

for value in ['a', 'ac', 'acc', 'accc', 'accd', 'acci', 'account_id', 'account_type', 'account_year', 'accs', 'acl', 'ae', 'af', 'afi', \
 'afn', 'aft', 'aid', 'al', 'ao', 'ap', 'arnopreviousyear', 'atotal', 'aunclassified', 'charname', 'currency', 'date_registered', \
 'date_removed', 'e', 'ec', 'ef', 'eff', 'efi', 'eft', 'efv', 'eg', 'em', 'ema', 'emo', 'eo', 'etotal', 'eunclassified', 'f', 'fe', 'fi', \
 'financial_year', 'fir', 'fiu', 'fo', 'fp', 'ftotal', 'funclassified', 'fye', 'fys', 'i', 'ic', 'ic100', 'ic110', 'ic121', 'ic125', 'ic132', \
 'ic140', 'ic161', 'ic162', 'ic163', 'ic171', 'ic175', 'ic180', 'ic300', 'ic500', 'ic600', 'ig', 'ig100', 'ig110', 'ig121', 'ig125', 'ig132', \
 'ig161', 'ig162', 'ig163', 'ig171', 'ig180', 'ig330', 'igi', 'igi700', 'igi710', 'igi720', 'igi730', \
 'io', 'iunclassified', 'iv', 'iv100', 'iv110', 'iv121', 'iv125', 'iv132', 'iv140', 'iv161', 'iv162', 'iv163', 'iv171', 'iv172', 'iv175', \
 'iv180', 'iv200', 'iv300', 'iv500', 'iv600', 'iv620', 'multiple', 'nb', 'nf', 'ni', 'no', 'ns', 'nv', 'oa', 'od', 'oe', 'of', 'og', 'oi', 'on', 'one', \
 'ono', 'onr', 'onu', 'oo', 'op', 'or', 'os', 'oso', 'osp', 'oss', 'osw', 'ou', 'ov', 'ox', 'oxa', 'oxb', 'oxd', 'oxe', 'period', 'phase', 'Funds_nonprofit', \
 'Funds_Business_sector', 'Funds_universities', 'Funds_NHS', 'Nongovernment_funding', 'Prop_nongov_funding']:
	df3.drop(columns=[value], inplace=True) # This line would drop unneeded columns if we wanted to at this stage - for now will pass the whole file out

df3 = df3[['Income2011-2012', 'Funds_general_public', 'Prop_general_public_funding', 'Government_funding', 'Prop_government_funding']]

print(list(df3))
print(df3.shape)

df3.to_json(path_or_buf='UKDA_data_cleaned.json', orient='index') # Save the dataframe out to a JSON in the format 'index' which is easy to read and verify manually
#df3.to_csv(path_or_buf='temp1.csv')

finishtime = datetime.datetime.now()
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"), '<<<') 