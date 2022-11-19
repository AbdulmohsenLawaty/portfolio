import time
from tracemalloc import start
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def display_data(df):
    """
        Ask the user if he wants to display 5 rows of the raw data and gives him the chance to display them more than once
        takes in the date frame we created 
    """
    #indices used to select the five rows and to keep track of them if the user wanted to see more
    start = 0
    end = 5

    while True:
        wants_or_not = input("Do you want to display 5 rows of data please type (yes or no): ").lower()
        if wants_or_not == 'yes' or wants_or_not =='no':
            break
    
    
    if wants_or_not == 'yes':

        while True:
            print(df.iloc[start:end])

            while True:
                wants_or_not = input("Do you want to dipslay 5 more rows of data please type (yes or no): ").lower()
                if wants_or_not == 'yes' or wants_or_not =='no':
                    break
           
            if wants_or_not == 'no':
                break

            start += 5
            end += 5
    print('-'*40)
               
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
    while True :
        
        city = input("Choose the city (chicago, new york city, washington): ").lower()
        if city not in CITY_DATA:
            continue
        break
        

    # get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'may', 'june']
    while True:
        
        month = input('Enter the name of the month you want to filter by, or (all) if you want no filter: ')
        month = month.lower()
        if month not in months:
            continue
        break


    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Enter the day if you want to filter by it , or (all) to apply no filter: ')
        day = day.lower()
        if day not in days:
            continue
        break
    
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    

    # filtering by given month
    df['month'] = df['Start Time'].dt.month_name()

    if month != 'all':
        df = df[df['month'] == month.title()]
    
    #filtering by given day
    df['day of week'] = df['Start Time'].dt.day_name()

    if day != 'all':
        df = df[df['day of week'] == day.title()]
        



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("most common month: ", df['month'].mode()[0])
    # display the most common day of week
    print("most common day: ", df['day of week'].mode()[0])

    # display the most common start hour
    print('most common start hour: ', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('most commonly used start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station

    print('Most commonly used End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    #grouped by the start station and end station, sorted based on the size of the result then printed the first result
    
     
    most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending = False).head(1)
    print('most frequent combination of start station and end station trip..\n', most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['total_travel_time'] = df['End Time'] - df['Start Time']
    print('Total travel time: ', df['total_travel_time'].sum())
    # display mean travel time
    print('mean travel time: ', df['total_travel_time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types: ',df['User Type'].value_counts())

    #checking if the city is washington to inform the user that it's data doesn't have gender of birth year information

    if city != 'washington':     
    # Display counts of gender
        print('\nCounts of gender' ,df['Gender'].value_counts())


        # Display earliest, most recent, and most common year of birth

        print('\nEarliest birth year: ',df['Birth Year'].min())
        print('Most recent birth year: ',df['Birth Year'].max())
        print('Most common birth year: ',df['Birth Year'].mode()[0])
    else:
        print("unfortunately the washignton data doesn't have information about gender or birth date of the users ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
