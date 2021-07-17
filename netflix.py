import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import tzlocal


def main():
    df = pd.read_csv('ViewingActivity.csv')
    desired_width = 100000
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', None)
    pd.options.mode.chained_assignment = None

    df = df.drop(
        ["Profile Name", "Attributes", "Supplemental Video Type", "Device Type", "Bookmark", "Latest Bookmark",
         "Country"],
        axis=1)
    df["Duration"] = pd.to_timedelta(df["Duration"])
    df = df[(df["Duration"] > "0 days 00:01:00")]

    df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)
    df = df.set_index("Start Time")
    time_zone = tzlocal.get_localzone().zone
    df.index = df.index.tz_convert(time_zone)
    df = df.reset_index()

    df["weekday"] = df["Start Time"].dt.weekday
    df["hour"] = df["Start Time"].dt.hour

    main_menu(df)


def main_menu(df):
    while True:
        # Showing the main menu
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


def time_spent():
    pass


def day_spent():
    pass


def hour_spent():
    pass


def select_show(df):
    selected_show = input("Enter show to check:  ")
    df["Duration"] = pd.to_timedelta(df["Duration"])
    selected_show_df = df[df["Title"].str.contains(selected_show, case=False, regex=False)]
    print("Total time spent watching", selected_show, "is", selected_show_df["Duration"].sum())
    time.sleep(2)
    by_day(selected_show_df, selected_show)
    time.sleep(2)
    by_hour(selected_show_df, selected_show)


def by_day(by_day_df, selected_show):
    by_day_df["weekday"] = by_day_df["Start Time"].dt.weekday
    by_day_df["hour"] = by_day_df["Start Time"].dt.hour

    # create office_by_day and count the rows for each weekday, assigning the result to that variable
    by_day_plot = by_day_df['weekday'].value_counts()

    # sort the index using our categorical, so that Monday (0) is first, Tuesday (1) is second, etc.
    by_day_plot = by_day_plot.sort_index()

    # optional: update the font size to make it a bit larger and easier to read
    mp.rcParams.update({'font.size': 22})

    # plot office_by_day as a bar chart with the listed size and title
    if selected_show is None:
        by_day_plot.plot(kind='bar', figsize=(20, 10), title="Total Viewings By Weekday")
    else:
        by_day_plot.plot(kind='bar', figsize=(20, 10), title="{} Viewings By Weekday".format(selected_show))
    # ('f model: T= {}'.format(t))
    mp.show()


def by_hour(by_hour_df, selected_show):
    by_hour_df['hour'] = pd.Categorical(by_hour_df['hour'],
                                        categories=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                                    17, 18, 19, 20, 21, 22, 23], ordered=True)

    # create office_by_hour and count the rows for each hour, assigning the result to that variable
    by_hour_plot = by_hour_df['hour'].value_counts()

    # sort the index using our categorical, so that midnight (0) is first, 1 a.m. (1) is second, etc.
    by_hour_plot = by_hour_plot.sort_index()

    # plot office_by_hour as a bar chart with the listed size and title
    if selected_show is None:
        by_hour_plot.plot(kind='bar', figsize=(20, 10), title="Total Viewings By Hour")
    else:
        by_hour_plot.plot(kind='bar', figsize=(20, 10), title="{} Viewings By Hour".format(selected_show))
    mp.show()


if __name__ == "__main__":
    main()
