#Cristina Logg PSET

#PART 1
#####################################################
#An API is a set of instructions for interfacing with software (getting it to talk with each other). This API is a set of instructions for getting into Twitter databases. Reading the documentation - we only have a week of tweets and random sampling.
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
    tweet_per_query = 80000, #
    tweet_max = 82000,
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
file_name = 'data/tweet_tryPSet.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 82000

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


#PART 2
########################################################
tweetdf = pd.read_json('/Users/cristinalogg/Desktop/github/big-data-spring2018/week-04/data/tweet_tryPset.json')
tweets.dtypes
tweets['location'].unique()

loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets.columns = ['count']
df_count_tweets
df_count_tweets.sort_index()

bos_list = tweets[tweets['location'].str.contains("Boston Ma$$")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("boston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("BOSTON")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Boston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Cambridge")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("cambridge")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("02139")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Chelsea")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Chelsea, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("ALLSTON")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Allston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("allston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Allston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Bo$ton")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("BOS")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("bos")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("BoStOn")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Brighton")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Brighton, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Brookline")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Brookline, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Charlestown")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Charlestown, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Chelsea")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Chelsea, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("chelsea")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Chelsea, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("CHELSEA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Chelsea, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("DORCHESTER")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Dorchester, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Dorchester")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Dorchester, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("everett")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Everett, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Everett")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Everett, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Fenway")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Gloucester")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Gloucester, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Harvard University")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Harvard Square")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Harvard Medical School")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("inman square")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Jamaica  Plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Jamaica Plain, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("jamaica  plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Jamaica Plain, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Lowell  ")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Lowell, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Lynn")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Lynn, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Malden")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Malden, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("malden")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Malden, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Massachusetts, USA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'MA, USA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Medford")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Medford, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("medford")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Medford, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("New York City")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'New York, NY', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Newtonville")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Newtonville, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Revere")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Revere, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Roslindale")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Roslindale, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Somerville")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Somerville, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("somerville")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Somerville, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("United States")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'USA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Watertown")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Watertown, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("watertown")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Watertown, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("West Roxbury")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'West Roxbury, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Allston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Allston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Arlington MA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Arlington, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Bo$ton")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Concord")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Concord, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Bos")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Davis Square")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Somerville, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("dorchester")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Dorchester, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("EVERETT")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Everett, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Jamaica Plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Jamaica Plain, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("jamaica plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Jamaica Plain, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Lowell")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Lowell, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Newton,")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Newton, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("MA, USA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Massachusetts', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Boston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("MIT")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Cambridge, MA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("Dha")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'Other Location', inplace = True)

bos_list = tweets[tweets['location'].str.contains("New England")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'New England, USA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("New Hampshire")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, 'New Hampshire, USA', inplace = True)

bos_list = tweets[tweets['location'].str.contains("New York")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets['location'].replace(bos_list, "New York, NY", inplace = True)

loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
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
# View the plot
plt.show()

#PART 3
########################################################
# Create a filter from df_tweets filtering only those that have values for lat and lon
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_geo)
len(tweets)

# Use a scatter plot to make a quick visualization of the data points
scatterplot_chart_1 = plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.title('Locations of Tweets')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()


#PART 4
######################################################
def get_tweets2(
    geo, #geo allows us to specify a Location via lat/long and radius
    out_file, #specify type of file to write to
    search_term = 'MBTA', #what search term are you interested in?
    tweet_per_query = 100, #
    tweet_max = 82000,
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
file_name = 'data/tweet_tryPSet_searching.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 82000

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

tweets_search = get_tweets2(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

tweetdf_search = pd.read_json('/Users/cristinalogg/Desktop/github/big-data-spring2018/week-04/data/tweet_tryPSet_searching.json')
tweets_search.dtypes

#PART 5
######################################################
tweets_search['location'].unique()

loc_tweets2 = tweets_search[tweets_search['location'] != '']
count_tweets2 = loc_tweets2.groupby('location')['id'].count()
df_count_tweets2 = count_tweets2.to_frame()
df_count_tweets2.columns = ['count']
df_count_tweets2
df_count_tweets2.sort_index()

bos_list2 = tweets_search[tweets_search['location'].str.contains("Boston Ma$$")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("boston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("BOSTON")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Boston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Cambridge")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Cambridge, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("cambridge")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Cambridge, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("02139")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Cambridge, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Chelsea")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Chelsea, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("ALLSTON")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Allston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("allston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Allston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Bo$ton")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("BOS")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("bos")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("BoStOn")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Brighton")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Brighton, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Brookline")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Brookline, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Charlestown")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Charlestown, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Chelsea")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Chelsea, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("chelsea")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Chelsea, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("CHELSEA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Chelsea, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("DORCHESTER")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Dorchester, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Dorchester")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Dorchester, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("everett")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Everett, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Everett")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Everett, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Fenway")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Gloucester")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Gloucester, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Harvard University")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Cambridge, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Harvard Square")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Cambridge, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Harvard Medical School")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("inman square")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Cambridge, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Jamaica  Plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Jamaica Plain, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("jamaica  plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Jamaica Plain, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Lowell  ")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Lowell, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Lynn")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Lynn, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Malden")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Malden, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("malden")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Malden, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Massachusetts, USA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'MA, USA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Medford")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Medford, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("medford")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Medford, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("New York City")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'New York, NY', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Newtonville")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Newtonville, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Revere")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Revere, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Roslindale")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Roslindale, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Somerville")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Somerville, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("somerville")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Somerville, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("United States")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'USA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Watertown")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Watertown, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("watertown")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Watertown, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("West Roxbury")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'West Roxbury, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Allston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Allston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Arlington MA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Arlington, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Bo$ton")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Concord")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Concord, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Bos")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Davis Square")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Somerville, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("dorchester")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Dorchester, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("EVERETT")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Everett, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Jamaica Plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Jamaica Plain, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("jamaica plain")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Jamaica Plain, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Lowell")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Lowell, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Newton,")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Newton, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("MA, USA")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Massachusetts', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("Boston")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Boston, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("MIT")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'Cambridge, MA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("New England")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'New England, USA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("New Hampshire")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, 'New Hampshire, USA', inplace = True)

bos_list2 = tweets_search[tweets_search['location'].str.contains("New York")]['location'] #for where tweets have location, create a mask, where the string within the locationcon
tweets_search['location'].replace(bos_list2, "New York, NY", inplace = True)


loc_tweets2 = tweets_search[tweets_search['location'] != '']
count_tweets2 = loc_tweets2.groupby('location')['id'].count()
df_count_tweets2 = count_tweets2.to_frame()
df_count_tweets2.columns = ['count']
df_count_tweets2
df_count_tweets2.sort_index()

# Create a list of colors (from iWantHue)
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

# Create a pie chart
plt.pie(df_count_tweets2['count'], labels=df_count_tweets2.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.title('Pie Chart of Tweets within 5 Miles of MIT containing "MBTA"')
plt.tight_layout()
# View the plot
plt.show()

#PART 6
######################################################
tweets_geo2 = tweets_search[tweets_search['lon'].notnull() & tweets_search['lat'].notnull()]
len(tweets_geo2)
len(tweets_search)

# Use a scatter plot to make a quick visualization of the data points
scatterplot_chart_2 = plt.scatter(tweets_geo2['lon'], tweets_geo2['lat'], s = 25)
plt.title('Locations of Tweets Containing the Words "MBTA"')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

#PART 7
######################################################
#Write to CSV both tweets and tweets_search
tweets[tweets.duplicated(subset = 'content', keep = False)]
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets.to_csv('twitter_data_part1_3.csv', sep=',', encoding='utf-8')

tweets_search[tweets_search.duplicated(subset = 'content', keep = False)]
tweets_search.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets_search.to_csv('twitter_data_part4_6.csv', sep=',', encoding='utf-8')

#EXTRA CREDIT
######################################################
import requests
import bs4
response = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_greenhouse_gas_emissions')
print(response.text)

soup = bs4.BeautifulSoup(response.text, "html.parser")
print(soup.prettify()) # Print the output using the 'prettify' function
# Access the title element
soup.title
# Access the content of the title element
soup.title.string
# Access data in the first 'p' tag
soup.p
# Access data in the first 'a' tag
soup.a
# Retrieve all links in the document (note it returns an array)
soup.find_all('a')
# Retrieve elements by class equal to link using the attributes argument
soup.findAll(attrs={'class':['mw-headline'])
# Retrieve a specific link by ID
soup.find(id="link3")
# Access Data in the table (note it returns an array)
soup.find_all('td')

  data = soup.findAll(attrs={'class':'flagicon'})
for i in data:
    print(i.string)

f = open('soup_extracredit.csv','a') # open new file, make sure path to your data file is correct

p = 0 # initial place in array
l = len(data)-1 # length of array minus one

f.write("Country, Emissions, Percentage\n") #write headers

while p < l: # while place is less than length
    f.write(data[p].string + ", ") # write city and add comma
    p = p + 1 # increment
    f.write(data[p].string + "\n") # write number and line break
    p = p + 1 # increment

f.close() # close file
