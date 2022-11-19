import time
import pandas as pd
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Using Anonymous function to check if the input is right
    check_city = lambda x : x in CITY_DATA
    check_day = lambda x: x in days
    check_month = lambda x: x in months
    print('Hello! Let\'s explore some US bikeshare data!')

    months = ['january', 'february', 'march', 'april', 'may', 'june','all']
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all']
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
    while not check_city(city):
        print('Please enter a valid city name')
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
    month = input('Which month? (January, February, March, April, May, June) or all\n').lower()
    while not check_month(month):
        print('Please enter a valid month')
        month = input('Which month? (January, February, March, April, May, June) or all\n').lower()
    day = input('Which day? (Sunday , Monday, Tuesday, Wednesday, etc...) or all\n').lower()
    while not check_day(day):
        print('Please enter a valid day')
        day = input('Which day? (Sunday , Monday, Tuesday, Wednesday, etc...) or all\n').lower()
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
        data - Pandas DataFrame containing city data filtered by month and day
    """
    data = pd.read_csv(CITY_DATA[city])
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['Month'] = data['Start Time'].dt.month_name()
    data['Day'] = data['Start Time'].dt.day_name()
    data['Hour'] = data['Start Time'].dt.hour
    if month != 'all':
        data = data[data['Month'] == month.title()]
    if day != 'all':
        data = data[data['Day'] == day.title()]
    return data
def time_stats(data):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        (dataframe) data - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month', end=' ')
    print(data['Month'].mode()[0])

    # display the most common day of week
    print('Most common day', end=' ')
    print(data['Day'].mode()[0])

    # display the most common start hour
    print('Most common Hour', end=' ')
    print(data['Hour'].mode()[0])
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)
def station_stats(data):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        (dataframe) data - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    print('Most common start station', end=' ')
    print(data['Start Station'].mode()[0])
    # display most commonly used end station
    print('Most common end station', end=' ')
    print(data['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    start, end = data.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most common route is ', end=' ')
    print(f'From ({start}) to ({end})')
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def trip_duration_stats(data):
    """
    Displays statistics on the total and average trip duration.
    Args:
        (dataframe) data - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    data['Trip Duration'] = data['Trip Duration'] // 60
    # display total travel time
    total_time = data['Trip Duration'].sum()
    avg_time = data['Trip Duration'].mean()
    print(f'Total Trips Time {total_time//60:.2f} Hours')
    # display mean travel time
    print(f'Average Trips Time {avg_time:.2f} minutes')

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def user_stats(data):
    """
    Displays statistics on bikeshare users.
    Args:
        (dataframe) data - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types there are two types of users subscribers and customers
    subscribers = data['User Type'].value_counts()['Subscriber']
    customers = data['User Type'].value_counts()['Customer']
    print(f'There are {subscribers} subscribers and {customers} customers')
    # Display counts of gender
    try:
        count_male = data['Gender'].value_counts()['Male']
        count_female = data['Gender'].value_counts()['Female']
        print(f'There are {count_male} male')
        print(f'There are {count_female} female')
    except:
        print('Your Data does not have "Gender" column')
    try:
        earliset = data['Birth Year'].min()
        most_recent = data['Birth Year'].max()
        common_year = data['Birth Year'].mode()[0]
        print(f'Earliest birth year is : {earliset}')
        print(f'Most recent birth year is {most_recent}')
        print(f'Most common birth year is {common_year}')
    except:
        print('Your Data does not have "Birth Year" column')
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def raw_data(data, count):
    '''
    To Display raw data for the user
    Args:
        (dataframe) data - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    '''
    command = input('Do you want to see raw data? Enter yes or no:\n').lower()
    if command == 'yes':
        print(data.iloc[count:count+5])
        count += 5
        raw_data(data, count)
    elif command == 'no':
        return
    else:
        print('Invalid input. Please try again.')
        raw_data(data, count)
        
def main():
    '''
    Driver function to run the program
    Calls all the functions (time_stats, station_stats, trip_duration_stats, user_stats, raw_data)
    Args:
        None
    Returns:
        None
    '''
    while True:
        city, month, day = get_filters()
        data = load_data(city, month, day)
        time_stats(data)
        station_stats(data)
        trip_duration_stats(data)
        user_stats(data)
        raw_data(data, 0)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
