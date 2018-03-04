gm#An API is a set of instructions for interfacing with software (getting it to talk with each other). This API is a set of instructions for getting into Twitter databases. Reading the documentation - we only have a week of tweets and random sampling.
import jsonpickle
import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

import os
#Change into subfolder as needed.
os.chdir('/Users/cristinalogg/Desktop/github/big-data-spring2018/week-04')
from twitter_keys import api_key, api_secret

auth = tweepy.AppAuthHandler(api_key, api_secret)
# wait_on_rate_limit and wait_on_rate_limit_notify are options that tell our API object to automatically wait before passing additional queries if we come up against Twitter's wait limits (and to inform us when it's doing so).
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)


#This is the scraper. This is how we get stuff and write it to a json file. Need to both get the stuff and parse it.

def get_tweets(
    geo, #geo allows us to specify a Location via lat/long and radius
    out_file, #specify type of file to write to
    search_term = '', #what search term are you interested in?
    tweet_per_query = 80, #
    tweet_max = 100,
    since_id = None, #allows you to create at the front end a manual window, so you can examine the json file and specify it as a sinceID in case you lose connection and have to redo it all over again.
    max_id = -1,
    write = False
  ):
  tweet_count = 0 #Collect a count of the number of tweets collected.
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max: #giant interator.
    try:
      if (max_id <= 0): #If under max, tell it to try to try the first if/else
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else: #are there new tweets?
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets: #for all new tweets, return tweet and add it to json file
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        if write == True:
            with open(out_file, 'w') as f:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n') #while a given out file is open and writeable 'w', pass it to the below line as f, write to the file the result of the tweet to a new json array.
      max_id = new_tweets[-1].id #maximum ID of the tweet we got last, every tweet has a unique ID.
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/tweet_trial2.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 100

#If you look at the json you can see a giant pile of crap... Now you know why you need to parse it. Also, look at it online via json viewer.
def parse_tweet(tweet):
  p = pd.Series()
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

tweetdf = pd.read_json('/Users/cristinalogg/Desktop/github/big-data-spring2018/week-04/data/tweet_trial2.json')
tweets.dtypes
tweets['location'].unique()

loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
df_count_tweets

df_count_tweets.sort_index()

# Create a list of colors (from iWantHue)
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

# Create a pie chart
plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()

# View the plot

# Create a filter from df_tweets filtering only those that have values for lat and lon
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_geo)
len(tweets)

# Use a scatter plot to make a quick visualization of the data points
plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.show()

bos_list = tweets[tweets['location'].str.contains("Boston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Cambridge")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)
bos_list = tweets[tweets['location'].str.contains("cambridge")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)
tweets['location'].unique()
bos_list = tweets[tweets['location'].str.contains("02139")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)
tweets['location'].unique()

plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()

tweets[tweets.duplicated(subset = 'content', keep = False)]
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets.to_csv('twitter_data.csv', sep=',', encoding='utf-8')
