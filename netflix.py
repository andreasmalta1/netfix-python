import pandas as pd
import numpy as np
import matplotlib.pyplot as mp

df = pd.read_csv('ViewingActivity.csv')
desired_width = 100000
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', None)
pd.set_option('col_header_justify', 'center')

df = df.drop(
    ["Profile Name", "Attributes", "Supplemental Video Type", "Device Type", "Bookmark", "Latest Bookmark", "Country"],
    axis=1)
df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)
df = df.set_index("Start Time")
df.index = df.index.tz_convert("Europe/Malta")
df = df.reset_index()
df["Duration"] = pd.to_timedelta(df["Duration"])
office = df[df["Title"].str.contains("The Office (U.S.)", regex=False)]
office = office[(office["Duration"] > "0 days 00:01:00")]
print(office["Duration"].sum())

office["weekday"] = office["Start Time"].dt.weekday
office["hour"] = office["Start Time"].dt.hour
office['weekday'] = pd.Categorical(office['weekday'], categories=[0, 1, 2, 3, 4, 5, 6], ordered=True)

# create office_by_day and count the rows for each weekday, assigning the result to that variable
office_by_day = office['weekday'].value_counts()

# sort the index using our categorical, so that Monday (0) is first, Tuesday (1) is second, etc.
office_by_day = office_by_day.sort_index()

# optional: update the font size to make it a bit larger and easier to read
mp.rcParams.update({'font.size': 22})

# plot office_by_day as a bar chart with the listed size and title
office_by_day.plot(kind='bar', figsize=(20, 10), title='Office Episodes Watched by Day')
manager = mp.get_current_fig_manager()
manager.full_screen_toggle()
mp.show()

# set our categorical and define the order so the hours are plotted 0-23
office['hour'] = pd.Categorical(office['hour'], categories=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                                            17, 18, 19, 20, 21, 22, 23], ordered=True)

# create office_by_hour and count the rows for each hour, assigning the result to that variable
office_by_hour = office['hour'].value_counts()

# sort the index using our categorical, so that midnight (0) is first, 1 a.m. (1) is second, etc.
office_by_hour = office_by_hour.sort_index()

# plot office_by_hour as a bar chart with the listed size and title
office_by_hour.plot(kind='bar', figsize=(20, 10), title='Office Episodes Watched by Hour')
mp.show()
