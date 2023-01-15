# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 10:08:08 2023

@author: Mohamed Ali
"""
import time
import pandas as pd

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
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ["chicago", "new york city", "washington"]
    city = input("please input city you will work on: ")

    while city not in city_list:
        print("currently only following citises are avaliable {chicago, new york city, washington}: " )
        city = input("please input city you will work on or type all: ")
        

    months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december', 'all']
    month = input("input the  month you are looking for (ex: january) or all: ")
    while month not in months_list:
        print("you need to type the word with lower case " )
        month = input("input correct month you are looking for (ex: january) or all: ")


    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']
    day =input("input the day you are looking for (ex:  monday) or all: ")
    while day not in day_list:
        print("you need to type the word with lower case: " )
        day = input("input correct day you are looking for (ex:  monday) or all: ")


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
    df = pd.read_csv(CITY_DATA[city], delimiter = ',')

    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] =  df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december']
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

    # TO DO: display the most common month
    df['month'] =  df['Start Time'].dt.month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december']

    popular_month_id = df['month'].value_counts().idxmax()
    popular_month = months[popular_month_id - 1]


    # TO DO: display the most common day of week
    df['day_of_week'] =  df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].value_counts().idxmax()


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()

    print("The most poular month is :", popular_month)
    print("The most poular day is :", popular_day)
    print("The most poular hour is :", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station

    popular_startst = df['Start Station'].value_counts().idxmax()


    # TO DO: display most commonly used end station

    popular_endst = df['End Station'].value_counts().idxmax()

    # TO DO: display most frequent combination of start station and end station trip
    popular_comb= df.groupby(['Start Station','End Station']).size().idxmax()

    print("The most commonly used start station is :", popular_startst)
    print("The most commonly used end station is :", popular_endst)
    print("The most frequent combination of start station and end station trip are :", popular_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df[['Start Time','End Time']] = df[['Start Time','End Time']].apply(pd.to_datetime)
    
    df['diff_times_hour'] = (df['End Time'] - df['Start Time'])/ pd.Timedelta(hours=1)
    df['diff_times_min'] = (df['End Time'] - df['Start Time'])/ pd.Timedelta(minutes=1)
    total_times_hour = round(df['diff_times_hour'].sum(),2)
    total_times_min = round(df['diff_times_min'].sum(),2)
    
    
    
    # TO DO: display mean travel time
    mean_times_hour = round(df['diff_times_hour'].mean(),2)
    mean_times_min = round(df['diff_times_min'].mean(),2)

    print("the Total travel time: ",total_times_hour,"Hour | which equal to ",total_times_min," Minute")
    print("the Mean travel time: ",mean_times_hour,"Hour | which equal to ",mean_times_min," Minute")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user_types = (df['User Type'].value_counts()).to_string()
        print("The counts of user types:\n"+user_types)
    except:
        print("Input data missing 'User Type' Information ...")


    # TO DO: Display counts of gender
    try:
        gender_count = (df['Gender'].value_counts()).to_string()
        ("\nThe counts of gender: \n"+gender_count)
    except:
        print("Input data missing 'Gender' Information ...")
   


    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_bd = df["Birth Year"].min()
        recent_bd = df["Birth Year"].max()
        commmon_bd = df["Birth Year"].mode()
        print("\nEarliest Year of birth: ",earliest_bd)
        print("most recent Year of birth: ",recent_bd)
        print("most common Year of birth: ",commmon_bd[0])
    except:
        print("Input data missing 'Birth Year' Information ...")
    
    
    

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
 
