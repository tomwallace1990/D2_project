#Created 28/9/18 by Vikki Richardson
#importing libraries for dealing with json, dataframes and the twitter api
#also imports personal credentials for twitter authorisation (kept seperately for security)

import tweepy
import json
import pandas as pd
from credentials import *
import datetime
import numpy as np

###################################################

#SET UP THE TWITTER AUTHENTICATION
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#creates an instance of tweepy api that automatically waits whenever we reach the rate limit 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(),wait_on_rate_limit='true',wait_on_rate_limit_notify='true')

###################################################

#BRING IN THE JSON FILE
#creates a dataframe with the json information produced in the previous section giving the scraped twitter handles
charityDF = pd.read_json('data_with_twitter_handles.json', orient ='index')

###################################################

#FUNCTION
#find the given twitter user and get their followers, follwing and number of tweets information
def try_get_user(s):
    print(s['Twitter Handle'])
    if s['Twitter Handle'] == '.':
        print('There was no handle')
        print('********************')
        s['Twitter followers'] = '.'
        s['Twitter following'] = '.'
        s['Number of tweets in total'] = 0
        return(s)    
    else:
        try:
            actualUserName = api.get_user(screen_name=s['Twitter Handle']) 
            print(actualUserName["followers_count"],actualUserName["friends_count"],actualUserName["statuses_count"]) 
            print('********************')
            s['Twitter followers'] = actualUserName["followers_count"]
            s['Twitter following'] = actualUserName["friends_count"]
            s['Number of tweets in total'] = actualUserName["statuses_count"]
            return(s)            
        except tweepy.TweepError as e:
            print(e)
            print('There was a failure')
            print('********************')
            s['Twitter followers'] = '.'
            s['Twitter following'] = '.'
            s['Number of tweets in total'] = 0
            return(s)              

###############################################

#MAIN
#creates a column to dictate whether there is a twitter handle or not
charityDF['Has Twitter'] = charityDF['Twitter Handle'].apply(lambda x: x != '.')            

#CALL TO DEFINED FUNCTION
#find the twittter user and assign the followers, following and number of tweets in total to the relevant columns
charityDF = charityDF.apply(try_get_user, axis = 1)

#SAVE THE DATA
#export the dataframe to json for further use
charityDF.to_json('data_with_twitter_info_only.json', orient='index')

################################################
