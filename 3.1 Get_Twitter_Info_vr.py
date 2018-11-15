#Created 28/9/18 by Vikki Richardson
#importing libraries for dealing with json, dataframes and the twitter api
#also imports personal credentials for twitter authorisation (kept seperately for security)

import tweepy
import json
import pandas as pd
from credentials import *
import datetime

print(' ') # Whitespace used to make the output window more readable
print('Run started at', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Header of the output, with the start time.
print(' ')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#creates an instance of tweepy api that automatically waits whenever we reach the rate limit 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(),wait_on_rate_limit='true',wait_on_rate_limit_notify='true')

#creates a dataframe with the json information produced in the previous section giving the scraped twitter handles
charityDF = pd.read_json('data_with_twitter_handles.json', orient ='index')

#creates a column to dictate whether there is a twitter handle or not
charityDF['Has Twitter'] = charityDF['Twitter Handle'].apply(lambda x: x != '.')

#creates a list of the twitter handles 
twitterHandlesList = charityDF["Twitter Handle"]

#creates blanks lists ready to be populated with the relevant twitter information for each charity
#we are looking specifically for followers, following and number of tweets
following_list = []
followers_list = []
number_of_Tweets = []

#sanity check to make sure we have iterated over all possible charities
numberOfFailedUsers = 0
numberOfSuccesses = 0


#find the given twitter user and get their followers, follwing and number of tweets information
def try_get_user(x):
    print(x, 'is x')
    if x == '.':
            #there was no twitter handle found previously
            failed_user(x)
    else:
        try:
            actualUserName = api.get_user(screen_name=x)                
            followers_list.append(actualUserName["followers_count"])
            following_list.append(actualUserName["friends_count"])
            number_of_Tweets.append(actualUserName["statuses_count"])
            global numberOfSuccesses 
            numberOfSuccesses = numberOfSuccesses + 1
        except tweepy.TweepError as e:
            print(e)
            failed_user(x)
            


def failed_user(userName):
    #either we didn't have a twitter handle to check or the twitter handle
    #we used wasn't found - we want to indicate this by populating lists with a 2'.'
    following_list.append('.')
    followers_list.append('.')
    number_of_Tweets.append(0) 
    global numberOfFailedUsers
    numberOfFailedUsers = numberOfFailedUsers + 1


for x in twitterHandlesList:
    try_get_user(x)
        
charityDF["Twitter followers"] = followers_list
charityDF["Twitter following"] = following_list
charityDF["Number of tweets in total"] = number_of_Tweets
charityDF = charityDF['Has Twittter','Twitter Handle','Twitter followers','Twitter following','Number of tweets in total']
charityDF.to_json(path_or_buf='data_with_twitter_info_only.json', orient='index')

#sanity check 
print("completed")
print(numberOfFailedUsers)
print("is the number of handles we couldn't find")
print(numberOfSuccesses)
print("is the number of twitter accounts we succesfully found info for")
print("Run finished at: "),datetime.datetime.now().strftime("%y-%m-%d %H:%M")