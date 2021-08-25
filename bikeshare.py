# This project uses Python to understand U.S. bikeshare data. An interactive environment will be created to calculate statistics for a dataset that will be filtered by the user.

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Here we will ask the user to input a city, month and day for their dataset

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
      city = input("\nPlease select a city to filter by: New York City, Chicago or Washington\n").lower()
      if city not in ('new york city', 'chicago', 'washington'):
        print("That is not a choice, please try again.")
        continue
      else:
        break

    # get user input for month (all, january, february, ... , june)
    while True:
      month = input("\nPlease select a month to filter by: January, February, March, April, May, June or All for all months?\n").lower()
      if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        print("That is not a choice, please try again.")
        continue
      else:
        break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day = input("\nPlease select a day to filter by: : Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All for all days.\n").lower()
      if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        print("That is not a choice, please try again.")
        continue
      else:
        break

    print('-'*40)
    return city, month, day

# Here we will create the dataframe based on the selections the user makes in the previous section
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data into the dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day from Start Time into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

# Here we will display the statistics about frequent travel times to the user
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_comm_month = df['month'].mode()[0]
    print('The most common month is:', most_comm_month)

    # display the most common day of week
    most_comm_day = df['day_of_week'].mode()[0]
    print('The most common day is:', most_comm_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_comm_start_hour = df['hour'].mode()[0]
    print('The most common start hour is:', most_comm_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Here we will display the statistics about station use to the user
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_comm_start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is:', most_comm_start_station)

    # display most commonly used end station
    most_comm_end_station = df['End Station'].value_counts().idxmax()
    print('\nThe most commonly used end station is:', most_comm_end_station)

    # display most frequent combination of start station and end station trip
    most_freq_station_combo = df.groupby(['Start Station', 'End Station']).count()
    print('\nThe most frequently used combination of start and end stations are:', most_comm_start_station, " and ", most_comm_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Here we will display the statistics about trip duration to the user
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('The total travel time is:', total_travel_time/60, " minutes, or ", total_travel_time/86400, "  days\n")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is:', mean_travel_time/60, " minutes, or ", mean_travel_time/86400, "  days\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Here we will display the statistics about bikeshare users (if available) to the user
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are:\n', user_types, '\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts()
        print('The counts of user gender are:\n', count_gender, '\n')
    else:
        print('There is no gender data for the selected filters.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_dob = int(df['Birth Year'].min())
        most_recent_dob = int(df['Birth Year'].max())
        most_comm_dob = int(df['Birth Year'].mode())
        print('The earliest year of birth is: ', earliest_dob)
        print('The most recent year of birth is: ', most_recent_dob)
        print('The most common year of birth is: ', most_comm_dob)
    else:
        print('There is no birth year data for the selected filters.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Here we ask the user if they want to view the raw data or restart the program
def raw_data (df):
    """Displays the filtered data 5 rows at a time"""
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_raw_data = input('\nWould you like to view first five rows of raw data? Enter yes or no.\n').lower()
            if view_raw_data != 'yes':
                break
            raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
