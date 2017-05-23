#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import re,string

#http://www.tweepy.org/
import tweepy

#Get your Twitter API credentials and enter them here
consumer_key = "Ly91EOyKaNYbqsBjT8u9bxkwp"
consumer_secret = "Iegj19PpM96oL6Ep0OofhiyjscNJkrd4noZJBxuJzt9oivNHxH"
access_key = "1125728827-WfJtDDmtMnQDW17cFwJxApCCUw3ynZHB5OeIGh6"
access_secret = "hmlEoEvbkEsjt8y0VSDAlypoYLbTtGGjGWjKwVvyTeVrl"

#method to get a user's last 100 tweets
def get_tweets(username):

    #http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

	#set count to however many tweets you want; twitter only allows 200 at once
    number_of_tweets = 100

	#get tweets
    tweets = api.user_timeline(screen_name = username,count = number_of_tweets)

	#create array of tweet information: username, tweet id, date/time, text
	#tweets_for_csv = [[username,tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]
    tweets_for_csv = [[tweet.text.encode("utf-8")] for tweet in tweets if tweet.lang == "en"]
    l = []
    for t in tweets_for_csv:
        l.append([str.lower(strip_all_entities(strip_links(t[0])))])
    
 
     #tweets_for_csv = [[tweet.text.encode("utf-8")] for tweet in tweets]
	#write to a new csv file from the array of tweets
    print "writing to {0}_tweets.csv".format(username)
    with open("{0}_tweets.csv".format(username) , 'w+') as file:
		writer = csv.writer(file, delimiter='|')
		writer.writerows(l)


def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')   
    text = text.replace('RT ', '')
        
    return text

def strip_all_entities(text):
    entity_prefixes = ['RT @','#', '@', 'RT@', 'rt@', 'rt @']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)



#if we're running this as a script
if __name__ == '__main__':

    #get tweets for username passed at command line
    if len(sys.argv) == 2:
        get_tweets(sys.argv[1])
    else:
        print "Error: enter one username"

    #alternative method: loop through multiple users
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)
