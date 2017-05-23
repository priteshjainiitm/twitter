# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 10:41:32 2017

@author: pj
"""
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('/home/pj/get_tweets/narendramodi_tweets.csv', names = ['tweet'])
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
ax.set_title('Wordcloud of Narendra Modi')
