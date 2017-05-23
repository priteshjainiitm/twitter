# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 10:56:30 2017

@author: pj
"""

import tweepy #https://github.com/tweepy/tweepy
import csv
import re,string
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


#Twitter API credentials
output_path = '/home/pj/get_tweets/'


consumer_key = "Ly91EOyKaNYbqsBjT8u9bxkwp"
consumer_secret = "Iegj19PpM96oL6Ep0OofhiyjscNJkrd4noZJBxuJzt9oivNHxH"
access_key = "1125728827-WfJtDDmtMnQDW17cFwJxApCCUw3ynZHB5OeIGh6"
access_secret = "hmlEoEvbkEsjt8y0VSDAlypoYLbTtGGjGWjKwVvyTeVrl"



def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
     auth.set_access_token(access_key, access_secret)
     api = tweepy.API(auth)
     
	
	#initialize a list to hold all the tweepy Tweets
     alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
     new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
     alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
     oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
     while len(new_tweets) > 0:
         print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
         new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
         alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
         oldest = alltweets[-1].id - 1
		
         print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
     outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
     l = []
     for t in outtweets:
        l.append([str.lower(strip_all_entities(strip_links(t[0])))])
    
    
     l = pd.DataFrame(l, columns = ["tweet"])
     s = output_path + str(screen_name) + '_tweets.csv'
     l.to_csv(s, index = False)
     df = l
     df = df.dropna()
     words = ' '.join(df['tweet'])
     wordcloud = WordCloud(
                      
                      stopwords=STOPWORDS,
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(words)


     f, ax = plt.subplots()
     ax.imshow(wordcloud)
     ax.axis('off')
     ax.set_title('Wordcloud of ' + str(screen_name))
     

     

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')   
    text = text.replace('RT ', '')
    text = text.replace('amp', '')
    text = text.replace('will', '')
        
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

if __name__ == '__main__':
	#pass in the username of the account you want to download
    get_all_tweets("yadavakhilesh")