import pandas as pd
import numpy as np
import matplotlib
%matplotlib inline
#If you get working directory issues try
#import os
#os.chdir('wk_dir_name_here')

#create a dataframe
df = pd.DataFrame()
print (df)

#first column, name, and add 3 rows with this data
df['name'] = ['Bilbo', 'Frodo', 'Drogon']

print(df)

#second column
df.assign(height = [0.5, 0.4, 0.6])

#Read a csv and import into a dataframe
df = pd.read_csv('/Users/cristinalogg/Desktop/github/big-data-spring2018/week-03/data/skyhook_2017-07.csv', sep=',')

#Print first 5 rows of the data frame.
df.head()
#length, width of dataset
df.shape

#get number of just columns
df.shape[1]

#get index of column names
df.columns

#What are the range of options? What values can the categories take on in the column cat_name?
##Categories of devices that are checking into the location based services API?
df['cat_name'].unique()

#hour is number of hours in the week, so ends at 167
#Asking Pandas what hours are 158. Get list of values.
#Made a mask- an array of true/false values,
#where the HOur = 158 is tested for each row for the hour column. Need to pass this mask again to the data frame
one_fifty_eight = df[df['hour'] == 158]
one_fifty_eight.shape

#interested in only those hour 158, but those rows where more than 50 checkins/GPS pings
#df[(df['hour'] == 158) & (df['count'] > 50)]
one_fifty_eight_high_activity = df[(df['hour'] == 158) & (df['count'] > 50)]
one_fifty_eight_high_activity.shape

#Create subset with Bastille day

bastille = df[(df['date'] == '2017-07-14')]
bastille.shape

# Mean of count - bastille['count'].mean()

#get a count of those with greater than average calls in a mask form
#bastille['count'] > bastille['count'].mean()

#need to pass into the data frame to apply it.
lovers_of_bastille = bastille[bastille['count'] > bastille['count'].mean()]

#Get summary statistics
lovers_of_bastille.describe()

#Sum all of the rows in the count column for each unitque date. Count of GPS pings per day. Run some common summary stats.
df.groupby('date')['count'].sum()
df.groupby('date')['count'].describe()
df['count'].max()
df['count'].min()
df['count'].mean()
df['count'].std()
df['count'].count()

#Return rows to me where the count is at the maximum
df[df['count'] == df['count'].max()]

#Not 24 hour times,
df['hour'].unique()
jul_sec = df[df['date'] == '2017-07-02']

jul_sec.groupby('hour')['count'].sum()


#convert date to more conventional date/time object
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#What day of the week is the weekday? Weekday function is Monday-Sunday and our Hours are Sunday to Saturday
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

#now need to figure out how to select 24 hour subsets for each one of the days. Drop columns outside the 24 hour window in a given day. Iterate thorugh the hours of the week, Taking 0-168 hours in the week and interating in 24 hours. Drop and create query that creates data frame of only the values we want to drop.
