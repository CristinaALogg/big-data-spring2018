# Problem Set 2: Intro to Pandas

Building off the in-class workshop, this problem set will require you to use some of Python's data wrangling functions and produce a few simple plots with Matplotlib. These plots will help us begin to think about how the aggregated GPS data works, how it might be useful, and how it might fall short.

## What to Submit

Create a duplicate of this file (`PSet2_pandas_intro.md`) in the provided 'submission' folder; your solutions to each problem should be included in the `python` code block sections beneath the 'Solution' heading in each problem section.

Be careful! We have to be able to run your code. This means that if you, for example, change a variable name and neglect to change every appearance of that name in your code, we're going to run into problems.

## Graphic Presentation

Make sure to label all the axes and add legends and units (where appropriate).

## Code Quality

While code performance and optimization won't count, all the code should be highly readable, and reusable. Where possible, create functions, build helper functions where needed, and make sure the code is self-explanatory.

## Preparing the Data

You'll want to make sure that your data is prepared using the procedure we followed in class. The code is reproduced below; you should simply be able to run the code and reproduce the dataset with well-formatted datetime dates and no erroneous hour values.

```python
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline

# Read in the data


df = pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')

# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5] #Adjustment factor, cannot just use i-5 as that gives negative numbers.
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
```

## Problem 1: Create a Bar Chart of Total Pings by Date

Your first task is to create a bar chart (not a line chart!) of the total count of GPS pings, collapsed by date. You'll have to use `.groupby` to collapse your table on the grouping variable and choose how to aggregate the `count` column. Your code should specify a color for the bar chart and your plot should have a title. Check out the [Pandas Visualization documentation](https://pandas.pydata.org/pandas-docs/stable/visualization.html) for some guidance regarding what parameters you can customize and what they do.

### Solution

```python
#Gather the sum of all ping counts by the new date detailed above.
date_count = df.groupby('date_new')['count'].sum()

#Create a bar chart with the Total GPS Pings by Date as title, assigned a color, and labeled axes.
figure = date_count.plot.bar(title="Total GPS Pings by Date", color='blue')
figure.set_xlabel("Date")
figure.set_ylabel("Number of GPS Pings")
```

## Problem 2: Modify the Hours Column

Your second task is to further clean the data. While we've successfully cleaned our data in one way (ridding it of values that are outside the 24-hour window that correspond to a given day of the week) it will be helpful to restructure our `hour` column in such a way that hours are listed in a more familiar 24-hour range. To do this, you'll want to more or less copy the structure of the code we used to remove data from hours outside of a given day's 24-hour window. You'll then want to use the [DataFrame's `replace` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.replace.html). Note that you can use lists in both `to_replace` and `value`.

After running your code, you should have either a new column in your DataFrame or new values in the 'hour' column. These should range from 0-23. You can test this out in a couple ways; the simplest is probably to `df['hour'].unique()`; if you're interested in seeing sums of total pings by hour, you can run `df.groupby('hour')['count'].sum()`.

### Solution

```python
# Create a new hour column.
# Determine which 24 hour block an hour given corresponds to.
# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.

#Want hours from 0-23, all i are 5 hours ahead of Boston time.
#Account for the 5 hour time difference between GMT and EST
for i in range(0, 168, 24):
  j = range(0,168)[i - 5]
  if (j > i):
    #From Email: Thanks for your note! You're actually super-close. The problem is that you're not quite replacing all possible values in the j > i branch; as it happens, the condition you specify in the else condition is actually the one you should be using to replace the remainder of the range in j > i condition. You'll then need a slightly different replace function in the else branch. Think of it like this: when j > i, that means that you're dealing with a day that's split across the beginning and the end of the range. So in addition to replacing 0 - 18 with 5 - 23, you need to replace 163 - 167 with 0 - 4. This is what the combination of the two replace statements you've written will do.
    df['hour'].replace(range(i, i+19), range(5, 24), inplace=True) #this is correct
    df['hour'].replace(range(j, j+5), range(0, 5), inplace=True)
    #df['hour'].replace(range(j, j + 5, 1), range(-5, 0, 1), inplace=True)
    #df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)
  else:
    #From Email: But when the hours are not split, you have a simpler task: replace the range that runs from j is (the bottom of the hour range for a given day, which is smaller than i by 5) to j + 24 (or i + 19) with the range that runs from 0 - 23.
    df['hour'].replace(range(j, i + 19), range(0, 24), inplace=True) #this is correct
    #df['hour'].replace(range(j, j + 24, 1), range(-5, 19, 1), inplace=True)

#Test to see if it works!
df['hour'].unique()
df.groupby('hour')['count'].sum()
#It works!! WOOHOO!
```

## Problem 3: Create a Timestamp Column

Now that you have both a date and a time (stored in a more familiar 24-hour range), you can combine them to make a single timestamp. Because the columns in a `pandas` DataFrames are vectorized, this is a relatively simple matter of addition, with a single catch: you'll need to use `pd.to_timedelta` to convert your hours columns to a duration.

### Solution

```python
#Convert hour field to unit hours via pandas to_timedelta
df['time_hours'] = pd.to_timedelta(df['hour'], unit='h')
#Create timestamp field that combines date_new (accounting for time change) and time_hours (accounting for time deltas)
df['timestamp'] = df['date_new'] + df['time_hours']

#Does it work?
print(df['timestamp'])
df.head()
#It works!
```

## Problem 4: Create Two Charts of Activity by Hour

Create two more graphs. The first should be a **line plot** of **total activity** by your new `timestamp` field---in other words a line graph that displays the total number of GPS pings in each hour over the course of the week. The second should be a **bar chart** of **summed counts** by hours of the day---in other words, a bar chart displaying the sum of GPS pings occurring across locations for each of the day's 24 hours.

### Solution

```python
#Line Plot, Total Activity by Timestamp Field
timestamp_count = df.groupby('timestamp')['count'].sum()

#Create a bar chart with the Total GPS Pings by Date as title, assigned a color, and labeled axes.
timestamp_line_chart = timestamp_count.plot(title="Total GPS Pings by Date", color='red')
timestamp_line_chart.set_xlabel("Time Stamp")
timestamp_line_chart.set_ylabel("Number of GPS Pings")

#Bar Chart of Summed Counts by Hour of Day
hour_bar_count = df.groupby('hour')['count'].sum()
figure = hour_bar_count.plot.bar(title="Total GPS Pings by Hour of the Day", color='green')
figure.set_xlabel("Hour of Day")
figure.set_ylabel("Total Number of GPS Pings")
```

## Problem 5: Create a Scatter Plot of Shaded by Activity

Pick three times (or time ranges) and use the latitude and longitude to produce scatterplots of each. In each of these scatterplots, the size of the dot should correspond to the number of GPS pings. Find the [Scatterplot documentation here](http://pandas.pydata.org/pandas-docs/version/0.19.1/visualization.html#scatter-plot). You may also want to look into how to specify a pandas Timestamp (e.g., pd.Timestamp) so that you can write a mask that will filter your DataFrame appropriately. Start with the [Timestamp documentation](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timestamps-vs-time-spans)!

```python
timeranges = df[(df.timestamp == '2017-07-01 14:00:00') | (df.timestamp == '2017-07-04 2:00:00') | (df.timestamp == '2017-07-05 8:00:00')]

#Draw scatterplot with size determined by GPS count
scatterplot_chart = plt.scatter(timeranges['lon'], timeranges['lat'], s=timeranges['count'])
plt.title('Number of GPS Pings in 2017 on July 1 at 2PM, July 4 at 2AM, and July 5 at 8AM')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
```

## Problem 6: Analyze Your (Very) Preliminary Findings

For three of the visualizations you produced above, write a one or two paragraph analysis that identifies:

1. A phenomenon that the data make visible (for example, how location services are utilized over the course of a day and why this might be).

EH: Yeahhhhh... as became abundantly apparent, this was not a property of the data but a mistake in the instructional material. C'est la vie. You did a pretty commendable job seeking order in madness, though. However, you seem to have only analyzed one of the visualizations...

I found it  interesting, in the bar chart entitled "Total GPS Pings by Hour of the Day", that the most pings are during the first three hours of the day.  I actually re-went through all of my code multiple times to make sure I was properly accounting for the 5 hour time change, and it appeared that I was. This makes me wonder why those time frames would have so many more pings than during the commuting/morning hours. I think that perhaps one explanation for this may be that people have their phones on energy saver mode when not plugged in - this mode can mean that phones do not ping GPS unless explicitly asked. As such, when people are moving about (i.e. commuting in the morning), their phones will not ping as much. Yet, when thinking of it this way, there is no reason why the evening commute times wouldn't also be reduced, which we do not see. Overall, I found this to be very curious and I would love to have the opportunity to further explore how Skyhook pulls GPS locations and under what circumstances they do so. In fact, I was interested enough, I looked at their documentation on their website and had little success in understanding this phenomenon.

2. A shortcoming in the completeness of the data that becomes obvious when it is visualized.

I think the fact that the dataset only contains hourly information and not minute/second may be an issue as more detailed hourly information can add more granular temporal detail in analysis than hourly information provides. When looking at the movement and location of people, granularity in time data is essential. Also, it would be interesting to know why there is a dip in the number of pings during the morning hours - was this a result of incomplete data gathering or was it a true observation?

3. How this data could help us identify vulnerabilities related to climate change in the greater Boston area.

Knowing not only where individuals live but congregate and move between (which may require individual IDs (by device) and timing to the minute/second) would help provide additional insight into what spaces are used by humans in living, working, and movement. It would also be great to map this data against the known weather patterns on those days - meaning if there was a massive storm on July 5th - what happens when flooding at a local level or even city-wide level occurs? Do people move away from Seaport or do they concentrate their locations within specific buildings? How long does it take to move between parts of Boston on sunny days versus rainy or snowy days? These are but a few of the questions that could be potentially answered with a more comprehensive dataset.
