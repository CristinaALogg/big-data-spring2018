import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline

# Read in the data

df = pd.read_csv('/Users/cristinalogg/Desktop/github/big-data-spring2018/week-03/data/skyhook_2017-07.csv', sep=',')

# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df.drop(df[
    (df['weekday'] == (i/24)) &
        (
            ( (df['hour'] < j) & (df['hour'] > i + 18) ) |
            ( (df['hour'] > i + 18 ) & (df['hour'] < j) )
            )
    ].index, inplace = True)
  else:
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    (df['hour'] < j) | (df['hour'] > i + 18 )
    )
    ].index, inplace = True)


## Problem 1: Create a Bar Chart of Total Pings by Date

###Your first task is to create a bar chart (not a line chart!) of the total count of GPS pings, collapsed by date. You'll have to use `.groupby` to collapse your table on the grouping variable and choose how to aggregate the `count` column. Your code should specify a color for the bar chart and your plot should have a title. Check out the [Pandas Visualization documentation](https://pandas.pydata.org/pandas-docs/stable/visualization.html) for some guidance regarding what parameters you can customize and what they do.

### Step 1 - Collapse by Date via groupby
date_count = df.groupby('date_new')['count']

#Show summary statistics by date
date_count.describe()

#Draft bar chart of pings (count) by date (date), Label Title and axes.

#dates.plot(title="Bar Plot of GPS Pings by Date")
date_count.plot(title="Total GPS Pings by Date")

#plt.plot(dates)
#plt.xlabel('Date')
#plt.ylabel('# of Pings')
#plt.legend()
#plt.show()

#myplot = dates.plot(kind='bar',legend=None,title="Total GPS Pings by Date")
#myplot.set_xlabel("Date")
#myplot.set_ylabel("Number of Pings")

#dates.plot(kind='bar', title = "Bar Plot of GPS Pings by Date")
#plotdates.set_xlabel("Date", fontsize=14)
#plotdates.set_ylabel("Number of Pings", fontsize = 14)
