import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello There! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Input for city (chicago, new york city, washington):").lower()
    while(city not in ['chicago','new york city','washington']):
        print(" ******* WRONG CITY NAME *******")
        city = input("Input for city (chicago, new york city, washington):").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Input for month (all, january, february, ... , june):").lower()
    while(month.lower() not in ['all','january', 'february', 'march', 'april', 'may', 'june']):
        print(" ******* WRONG Month *******")
        month = input("Input for month (all, january, february, ... , june):").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Input for day of week (all, monday, tuesday, ... sunday):").lower()
    while(day.lower() not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']):
        print(" ******* WRONG Day *******")
        day = input("Input for day of week (all, monday, tuesday, ... sunday):").lower()

    print('-'*40)
    return city, month, day


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


    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    print("The most common {} : {}".format("month",df['Start Time'].dt.month.mode()[0]))

    # display the most common day of week
    print("The most common {} : {}".format("week",df['Start Time'].dt.weekday_name.mode()[0]))

    # display the most common start hour
    print("The most common {} : {}".format("start hour",df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common {} : {}".format("Start Station",df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most common {} : {}".format("End Station",df['End Station'].mode()[0]))   

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip : {}".format((df['Start Station'] + ' ----> '+ df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time : {}".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("Mean travel time: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nCounts of user types:")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if('Gender' in df.index):
        print("\nCounts of gender:")
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if('Birth Year' in df.index):
        print("\nEerliest year of birth:")
        print(int(df['Birth Year'].min()))
       
        print("\nMost recent year of birth:")
        print(int(df['Birth Year'].max()))

        print("\nCommon year of birth:")
        print(int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        rawdata = input('\nAre you interested to see the raw data? Enter yes or no.\n').lower()
        while(rawdata not in ['yes','no']):
            print(" ******* WRONG ANSWER *******")
            rawdata = input('\nAre you interested to see the raw data? Enter yes or no.\n').lower()
        index=range(0,len(df.index),5)
        for i in index:
            if(rawdata == 'yes'):
                print(df.iloc[i:i+5])
                rawdata = input('\nAre you interested to see the raw data? Enter yes or no.\n').lower()
                while(rawdata not in ['yes','no']):
                    print(" ******* WRONG ANSWER *******")
                    rawdata = input('\nAre you interested to see the raw data? Enter yes or no.\n').lower()
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
