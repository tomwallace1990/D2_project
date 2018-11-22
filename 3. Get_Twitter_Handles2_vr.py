#Create 28/9/18 by Vikki Richardson
#importing libraries for opening urls and parsing the html, reading json and creating dataframes

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import parse
import pandas as pd 
import json
import csv


#########################################################
#BRING IN THE JSON FILE

#Read the json file created by Tom in the previous web scraping action to update our original charities data
charityDF = pd.read_json('new_scrape_data.json', orient ='index')

##########################################################

#FUNCTION
#function take a url and try to open the page, parse the information and return a twitter handle.
#If this fails a '.' placeholder is returned instead
def getTwitterHandle(x):
    print(x)
    if x == '.':
        print('****************')
        return('.')
    else:
        try:
            #open up the relevant webpage (giving 20 seconds before failing)         
            html_page = urlopen(x, timeout=20)
            #create a BS object with the relevant web page
            soup = BeautifulSoup(html_page, features='lxml')
            #finds all the href instances on the current page that contain twitter in the link
            handle = [ a["href"] for a in soup.find_all("a", href=True) if("twitter" in a["href"])]
            #keep track of the number of href instances we have in order that the list can be iterated over
            #and manipulated depending on what the results are per iteration
            handleSize = len(handle)
            #if there are no hrefs it follows there are no twitter handles, keep note of the number of fails
            if handleSize == 0:
                print('******************')
                return('.')
            else:
                #for each href do the following:
                for twits in handle:
                    #as we iterate over the href list and find hrefs that don't fit the criteria we manually reduce the handleSize.  This
                    #is done as a sanity check in order that we definitely iterate over every href as necessary
                    if handleSize == 0:
                        #means we had a list of hrefs, have checked them all and nothing is relevant so we can't find a twitter handle
                        #we want to end the for loop here
                        print('*****************')
                        return('.')
                    else:
                        #check the first item in the handle array which should be a url with twitter.com in it
                        url = twits
                        #get the path from the url so stripping away the extraneous http://twiiter.com info
                        path = parse.urlparse(url).path 
                        #looks to see if they haven't shortened the twitter address and it has #! in it - if so need to use fragment
                        if path == "/":
                            path = parse.urlparse(url).fragment
                        #if any of these keywords are in the path it is unlikely to give us a proper twitter handle without doing extra investigation
                        #that is probably outwith the scope of this project so we just want to assume this is not the relevant twitter handle
                        if 'search' in path or 'home' in path or 'archives' in path or 'tweet' in path or 'share' in path or 'intent' in path or 'twitter' in path:
                            #we have to check for handleSize again as we iterate through the handle array
                            #if there are entries in the array that are not suitable we want to check the next instance
                            #at that point we reduce handleSize in order that we can break from the loop or continue when necessary
                            #when handleSize reaches zero we can accept we have found no suitable hrefs and therfore add a "." to the handles list
                            if handleSize > 0:
                                #reduces handleSize 
                                handleSize = handleSize - 1
                                #accounts for last instance of the href array being iterated over
                                if handleSize == 0:
                                    print('******************')
                                    return('.')
                            else:
                                #if handleSize is now zero we can assume there are no relevant hrefs
                                #as we have iterated through our entire href array.  Continuing here leads us directly to the beginning of the for loop 
                                #and handleSize == 0 will be dealt with appropriately
                                continue
                        else:
                            #checks if using fragment with a ! and if so we should use everything that comes after this as the path
                            if path[0] == "!":
                                path = path[2:]
                            else:        
                                path = path[1:] 
                            #if there is a / in the path we need to extract the twitter handle which is generally the text before the /
                            if "/" in path:
                                path = path.split("/")[0] 
                            #we have found a relevant twitter handle.  We only want one per website so now we can break the loop
                            #for this website
                            print(path)
                            print('******************')
                            return(path)
                          
                        
        except Exception as e:
            #we want one entry per charity so add a "." to the handles array if we cant open the url for whatever reason
            print(e)
            print('********************')
            return('.')


##############################################

#MAIN
#CALL TO DEFINED FUNCTION
#create a new column called Twitter Handle that will hold the twitter handle found using the defined function
charityDF['Twitter Handle'] = charityDF['Website'].apply(getTwitterHandle) 

#SAVING THE DATA
#the new dataframe only needs contain the index (charity number), the website info and the twitter handle
charityDF = charityDF[['Website', 'Twitter Handle']]
#make a json file with the newly scraped info for use in the next script 
charityDF.to_json('data_with_twitter_handles.json', orient='index')

###############################################
