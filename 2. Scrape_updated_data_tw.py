#Scrape updated data from Charity Commission website
#Tom Wallace
#5/10/18
#This file reads in the JSON from 'Read_csv_to_JSON_tw.py' as a pandas dataframe and then scrapes the 2017 income and expenditure of each charity form the charity commission website. 
#It then creates a new JSON file with the new data which can be easily appended onto the origional data as shown in 'Combine_old_and_new_data.py'. 
#Some of this data is avalable in database format (.BCP files) which I don't know how to read - hence the webscrape.

################################# Import packages #################################
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import time
from time import sleep
import datetime
import random
import json
import pandas as pd
import os.path
import re

################################# Functions #################################

def moneyconverter(money):

	if 'M' in money.text: # Convert the money from '16.5M' to 16500000 so it can be held as an int
		money = money.text.replace('£', '') #Remove string characters
		money = money.replace('.', '')
		money = money.replace('M', '')
		moneytext = money + '00000' # Add the correct number of zeros
	elif 'K' in money.text:
		money = money.text.replace('£', '')
		money = money.replace('.', '')
		money = money.replace('K', '')
		moneytext = money + '00'
	else:
		print('*** WARN! Charity number: ' , charno,  'income format error ***') # Warn the user if there is a format problem.
	return (moneytext)

def textformatter(text, string):
	text = text.replace(string,'') # Strip off the title text.
	text = text.replace('\n', '') # Strip new lines.
	text = text.replace('\t', '') # Strip tabs.
	text = text.replace('/', ' or ') # Replace forward slash, whcih is a JSON relevant character, with 'or'.
	text = text.split('\r') # Make the block of text into a list, seperating elements by the return character.
	text = list(filter(None, text)) # There are blank lines in the origional blck so this line deletes empty elements from the list.
	return(text)

def sleepytime(incometext_list, exptext_list, charno_list, finyeartext_list, trustee_list, staff_list, volunteers_list, companyno_list, survived_list, website_list, what_list, who_list, how_list):
	incometext_list = list(map(lambda x :int(x), incometext_list)) 
	exptext_list = list(map(lambda x :int(x), exptext_list)) 
	charno_list_dump = charno_list[:count] # Charity number is a bit different as it is not appended each time so this selects it from the list based on the count number of the run
	dicto_part={'ccnum':charno_list_dump, 'updated_income':incometext_list, 'Updated_expenditure':exptext_list, 'Financial_year_ending':finyeartext_list, 'Trustees':trustee_list, 'Staff':staff_list, 'Volunteers':volunteers_list, 'Company number':companyno_list, \
		'Survived':survived_list, 'Website':website_list, 'What the charity does':what_list, 'Who the charity helps':who_list, 'How the charity works':how_list} # Store the new variables as a dictionary
	df_part = pd.DataFrame(dicto_part) # Convert the dictionary to a pandas dataframe
	df_part.set_index(['ccnum'], inplace=True) # Set the index of the data frame as charity number
	starttime_str = starttime.strftime("%Y-%m-%d") # Grab the start time to add to the filename
	dumppath = './Partial_dumps' # Set the path for the data dump.
	if not os.path.exists(dumppath): # If that path doesn't exist then make it.
		os.makedirs(dumppath)
	dumpfilepath = dumppath + '/partial_dump' + starttime_str + '.json' # Concatenate the dump file path
	df_part.to_json(path_or_buf=dumpfilepath, orient='index') # Save the dump dataframe out to a JSON

	sleeptime = 100 + random.randint(1,60) # Generate a sleep time with some randomness to make the scrape look less systematic.
	longsleeptime = datetime.datetime.now() # Grab the current time.
	sleeptime1 = time.strftime('%H:%M:%S', time.gmtime(sleeptime)) # Turn the sleep time into a time/date object.
	resumetime = longsleeptime + datetime.timedelta(0,sleeptime) # Calculate when the program will resume.
	print('Records up to processing number', count, 'dumped to disk') # Print info for the user
	print('Sleeping for', sleeptime1, 'at', longsleeptime.strftime("%H:%M:%S"), 'resuming at', resumetime.strftime("%H:%M:%S")) # Print the time info.
	print(' ')
	sleep(sleeptime) # Sleep

################################# Scraper function #################################
def scrapeorg(charno): # This defines the charity scraper fucntion - this get's looped over so everything is individual charity level. The main program is below.

	charno=str(charno) # Trun the charity number into a string so it can be concatinated into a URL.

	pubregister = 'http://beta.charitycommission.gov.uk/charity-details/?regid=' # This is the base URL for the charity commission's database.

	webbaddress = pubregister + charno + '&subid=0' # Generate a varaible holding each individual charity page by concatenating stings.

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'} # Spoof the user-agent of the request to return the content seen by Chrome.
	
	rorg = 0
	errorcount=0

	while rorg==0:
		try:
			rorg = requests.get(webbaddress, headers=headers)
		except:
			print('Disconnected, sleeping for 5 seconds')
			sleep(5)
			errorcount = errorcount + 1
			if errorcount==3:
				print('Multiple disconnections, sleeping for 100 mins')
				sleep(100*60)
				errorcount=0
			else:
				pass

	try: # This try block wraps the entire parse. If the charity has been removed they still have a page which is mostly blank and the parse will fail. They will then be given missing values intead.
		html_org = rorg.text # Get the text elements of the page.
		soup_org = soup(html_org, 'html.parser') # Parse the text as a BS object.

		money = soup_org.find_all("span", class_="big-money") # Find all of the large money text.
		income = money[0] # Income is always the first element.
		incometext = moneyconverter(income)
		expend = money[1] # Expenditure is always the second element.
		exptext  = moneyconverter(expend)

		name1 = soup_org.find("div", class_="charity-heading-panel") # Get the name, just for the output window and cross-checking - it is identical to the name already in the origional data.
		name = name1.find("h1") # Name is a bit deeper so need a second line to grab 'h1' inside 'charity-heading-panel'.
		nametext = name.text

		finyear1 = soup_org.find("div", class_="charity-heading-panel") # get the financial year the record pertains to - mostly for cross-checking and validaiton.
		finyear = finyear1.find("em") # Again needs a deeper dive into the tags
		finyeartext = finyear.text

		try: # Not all charities have this information so it has it's own try/except block which can gen missing values if it's not found rather than tripping the main try/except.
			whatwhohow = soup_org.find('div', id='plWhatWhoHow', class_='detail-panel') # Need to go deeper into the tags to get these.
			whatwhohow = whatwhohow.find_all('div', class_='detail-panel-wrap')

			what = whatwhohow[0].text # What is always element 0.
			what = textformatter(what,'What the charity does')
			
			who = whatwhohow[1].text # Who is element 1
			who = textformatter(who,'Who the charity helps')
			
			how = whatwhohow[2].text # how is element 2
			how = textformatter(how,'How the charity works')

		except:
			what = '.' # Set missing to a period.
			who = '.'
			how = '.'
			print('*** WARN! Charity number: ' , charno,  'Area info error ***') # Warn the user

		try:
			staff = soup_org.find("div", class_="detail-25") # Get staff numbers info
			staff = staff.find('span', class_='small-header', text='Employees') # Get all the text the numbers are held in
			staff = staff.previous_sibling
			staff = staff.text
			staff = int(staff)
		except:
			staff = 0

		try:
			trustee = soup_org.find("div", class_="detail-25") # Get staff numbers info
			trustee = trustee.find('span', class_='small-header', text='Trustees') # Get all the text the numbers are held in
			trustee = trustee.previous_sibling
			trustee = trustee.text
			trustee = int(trustee)
		except:
			trustee = 0

		try:
			volunteers = soup_org.find("div", class_="detail-25") # Get staff numbers info
			volunteers = volunteers.find('span', class_='small-header', text='Volunteers') # Get all the text the numbers are held in
			volunteers = volunteers.previous_sibling
			volunteers = volunteers.text
			volunteers = int(volunteers)
		except:
			volunteers = 0

		try:
			companyno = soup_org.find("div", id='ContentPlaceHolderDefault_cp_content_ctl00_CharityDetails_4_TabContainer1_tpOverview_plCompanyNumber', class_="charity-no") # Grab the company ID for charities which have it.
			companyno = companyno.text # Get just the text.
			companyno = companyno.replace('Company no.','') # Remove the title.
			companyno = companyno.replace('\n', '') # Strip new lines.
			companyno = companyno.replace('\t', '') # Strip tabs.
			companyno = companyno.replace('\r', '') # Strip returns.
			companyno = companyno.replace(' ', '') # Strip empty space.
		except:
			companyno = -99 # Set missing to an int so the variable can be kept as an int when the charities are combined togethor at the end.    

		try:
			website = soup_org.find_all("div", class_="detail-33")
			website = website[1]
			website = website.find('a', href= re.compile('http'))
			website = website.text 
		except:
			website = '.'
	
		survived=1 # Generate a variable tracking if the charity survived - if they have and up to date record they survived. If this function goes to 'except' they died.
		statustext = "Charity found" # Generate status text for the output window if above is sucessful.

		return (incometext, nametext, webbaddress, finyeartext, statustext, exptext, survived, trustee, staff, volunteers, what, who, how, companyno, website) # Push the generated variables back to the main program

	except Exception as e: # If the prase fails, generate fault information and set variables to missing values - this charity died or was removed.
		typetext = (str(type(e))) # This indicates the type of error.
		etext = (str(e)) # This is the details of the error.

		incometext, companyno, exptext = -99, -99, -99
		trustee, staff, volunteers, survived = 0, 0, 0, 0
		nametext, finyeartext, what, who, how, website = ".", ".", ".", ".", ".", "."

		statustext = "*** WARN! " + typetext + ": " + etext + " ***" # Format status to be shown to user

		return (incometext, nametext, webbaddress, finyeartext, statustext, exptext, survived, trustee, staff, volunteers, what, who, how, companyno, website) # Push the missing value variables back to the main program

################################# Main program #################################

starttime = datetime.datetime.now() # Grab the date and time for when the run stated.
print(' ') # Whitespace used to make the output window more readable
print('>>> Run started at', starttime.strftime("%Y-%m-%d %H:%M:%S") , ' <<<') # Header of the output, with the start time.
print(' ')

count=0 # Create count variable which is used in the validation at the end of the program run.

df1 = pd.read_json(path_or_buf='charity_oneyear.json', orient ='index') # Read in the JSON file of the main data set as created in 'Read_csv_to_JSON_tw.py' as a pandas data frame.

charno_list = df1.index.values.tolist() # Get the charity numbers form the dataframe index so they can be fed to the scraper function.
charno_list_len = len(charno_list) # Store the length of the list of charity numebrs - used in validation and calculating statistics at the end of the program run.

incometext_list, finyeartext_list, statustext_list, exptext_list, trustee_list, staff_list, volunteers_list, survived_list, what_list, who_list, how_list, companyno_list, \
 website_list = [], [], [], [], [], [], [], [], [], [], [], [], [] # make empty lists for appending the data coming from the scraper

for charno in charno_list: # For each row in the list created above from the data frame index.
	incometext, nametext, webbaddress, finyeartext, statustext, exptext, survived, trustee, staff, volunteers, what, who, how, companyno, website = scrapeorg(charno) # Feed the funciton each charity number in turn and pickup the returns from the fucntion.
	
	for var, var_list in zip([incometext, finyeartext, statustext, exptext, survived, trustee, staff, volunteers, what, who, \
	 how, companyno, website], [incometext_list, finyeartext_list, statustext_list, exptext_list, survived_list, trustee_list, staff_list, volunteers_list,  what_list, who_list, how_list, companyno_list, website_list]):
		var_list.append(var)	

	count=count+1 # Incrament the count.
	print('---------------------------------------------------------------------------') # Print the results of each loop for the user to monitor
	runtime = datetime.datetime.now() # Print the current time for each run.
	percdone = (count+1)/charno_list_len*100 # Calculate the percentage complete
	print('Prcoessing number:',count, ' | ', 'Time stamp:', runtime.strftime("%H:%M:%S"),' | ', 'Elapsed time:', runtime-starttime, ' | ' "%.2f" % percdone, '% done')
	print('+++', statustext, '+++')
	print(webbaddress)
	print('Charity number: ',charno)
	print('Name: ',nametext)
	print('---------------------------------------------------------------------------')
	print(' ')
	
	if count % 10 == 0: # To avoid overloading the server or getting banned, sleep every 100 charities scraped. Through experimentation this was deemed a better strategy than having a shorter sleep on every run. This block also saves the current results out in case the run fails later.
		sleepytime(incometext_list, exptext_list, charno_list, finyeartext_list, trustee_list, staff_list, volunteers_list, companyno_list, survived_list, website_list, what_list, who_list, how_list)
	else:
		pass

error_count = survived_list.count(0) # Count how many survived to generate end of run validation stats

incometext_list = list(map(lambda x :int(x), incometext_list)) 
exptext_list = list(map(lambda x :int(x), exptext_list)) 

dicto={'ccnum':charno_list, 'updated_income':incometext_list, 'Updated_expenditure':exptext_list, 'Financial_year_ending':finyeartext_list, 'Trustees':trustee_list, 'Staff':staff_list, 'Volunteers':volunteers_list, 'Company number':companyno_list, \
 'Survived':survived_list, 'Website':website_list, 'What the charity does':what_list, 'Who the charity helps':who_list, 'How the charity works':how_list} # Store the new variables to be appended to the data as a dictionary

df2 = pd.DataFrame(dicto) 
df2.set_index(['ccnum'], inplace=True)
df2.to_json(path_or_buf='new_scrape_data.json', orient='index')

finishtime = datetime.datetime.now() # Grab the finish time.
detlatime = finishtime-starttime # Work out how long the run took.
print('>>> Finished run at' , finishtime.strftime("%H:%M:%S"),'|' , 'Run took', detlatime, '|', count , 'of' ,charno_list_len, 'charities processed <<<') # Show the time at the end of the run and how many charities were processed - this should always equal the input n since the program is robust to errors
print('>>>',error_count ,'returned no financial information <<<') # Show the number of charities which did not have information avalable - these are dead Jim
print('>>>',100-((error_count/charno_list_len)*100) ,'% of records were successfully updated <<<') # Using the error count, calculate the percentage of records which were sucessfully retrived and updated