# A program that loads a ViewingActivity.csv file downloaded from Netflix.
# The program shows a menu that allows the user to select four options:
# 1. View your total viewing time on Netflix
# 2. Check your viewing activity by day of the week
# 3. Check your viewing activity
# 4. Search for a show/movie and view the total viewing time and viewing activity by day and hour for that show
# 5. Exit the program

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import tzlocal


# Main program function
def main():
    # Reading the csv file as a data frame and arranging it
    df = pd.read_csv('ViewingActivity.csv')
    desired_width = 100000
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', None)
    pd.options.mode.chained_assignment = None

    # Removing unnecessary columns from the data frame
    df = df.drop(
        ["Profile Name", "Attributes", "Supplemental Video Type", "Device Type", "Bookmark", "Latest Bookmark",
         "Country"],
        axis=1)
    # Changing the duration column to elapsed time and selecting only viewing times greater than one minute to remove
    # trailers watched
    df["Duration"] = pd.to_timedelta(df["Duration"])
    df = df[(df["Duration"] > "0 days 00:01:00")]

    # Setting the start to the local time using the tz module
    df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)
    df = df.set_index("Start Time")
    time_zone = tzlocal.get_localzone().zone
    df.index = df.index.tz_convert(time_zone)
    df = df.reset_index()

    # Adding a column weekday
    df["weekday"] = df["Start Time"].dt.weekday
    # Adding a column hour
    df["hour"] = df["Start Time"].dt.hour

    # Calling the main menu
    main_menu(df)


# Function showing the main
def main_menu(df):
    while True:
        print("----MENU-----")
        print("1. View total time spent")
        print("2. View by day")
        print("3. View by hour")
        print("4. View by show")
        print("5. Exit")
        # Collecting user choice
        response = input("Choice: ")

        # Checking user selection. If selection is invalid program loops until a valid selection is inputted
        if response == "1":
            # When 1 is selected the sum of the duration is shown as the total viewing time
            df["Duration"] = pd.to_timedelta(df["Duration"])
            print("Total Time spent on Netflix is", df["Duration"].sum())
            time.sleep(3)
        elif response == "2":
            by_day(df, None)
        elif response == "3":
            by_hour(df, None)
        elif response == "4":
            select_show(df)
        elif response == "5":
            break
        else:
            print("Invalid Choice")


# Function allowing the user to search for a particular show
def select_show(df):
    # Receiving the user input
    selected_show = input("Enter show to check:  ")
    # Filter by searched show without matching the case
    selected_show_df = df[df["Title"].str.contains(selected_show, case=False, regex=False)]
    # Printing the total viewing for the chosen
    print("Total time spent watching", selected_show, "is", selected_show_df["Duration"].sum())
    time.sleep(2)
    # Calling the by_day and by_hour functions passing the filtered data frame and the selected show name
    by_day(selected_show_df, selected_show)
    time.sleep(2)
    by_hour(selected_show_df, selected_show)


# The by_day function shows the users their viewing habits by day of the week
# This function can be called through the main menu or when selecting a show
# When called from the main_menu, the selected_show name is None and the full data frame is passed
# When called after selecting a show, the filtered data frame and name of the show are passed
def by_day(by_day_df, selected_show):
    # Set the categorical and define the order so the days are plotted Monday-Sunday
    by_day_df["weekday"] = pd.Categorical(by_day_df["weekday"], categories=[0, 1, 2, 3, 4, 5, 6], ordered=True)
    # Count the rows for each weekday
    by_day_plot = by_day_df["weekday"].value_counts()
    # Sort the index with Monday (0) is first, Tuesday (1) is second, etc.
    by_day_plot = by_day_plot.sort_index()
    mp.rcParams.update({'font.size': 22})

    # Plot the result as a bar chart
    if selected_show is None:
        by_day_plot.plot(kind='bar', figsize=(20, 10), title="Total Viewings By Weekday")
    else:
        by_day_plot.plot(kind='bar', figsize=(20, 10), title="{} Viewings By Weekday".format(selected_show))
    mp.show()


# The by_hour function shows the users their viewing habits by hour of the day
# This function can be called through the main menu or when selecting a show
# When called from the main_menu, the selected_show name is None and the full data frame is passed
# When called after selecting a show, the filtered data frame and name of the show are passed
def by_hour(by_hour_df, selected_show):
    # Set the categorical and define the order so that hours are plotted from midnight to 23:00pm
    by_hour_df['hour'] = pd.Categorical(by_hour_df['hour'],
                                        categories=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                                    17, 18, 19, 20, 21, 22, 23], ordered=True)

    # Count the rows for each hour
    by_hour_plot = by_hour_df['hour'].value_counts()
    # Sort the index with midnight (0) is first, 1 a.m. (1) is second, etc.
    by_hour_plot = by_hour_plot.sort_index()

    # Plot the result as a bar chart
    if selected_show is None:
        by_hour_plot.plot(kind='bar', figsize=(20, 10), title="Total Viewings By Hour")
    else:
        by_hour_plot.plot(kind='bar', figsize=(20, 10), title="{} Viewings By Hour".format(selected_show))
    mp.show()


if __name__ == "__main__":
    main()
