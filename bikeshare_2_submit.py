import time
import pandas as pd
import numpy as np
import math

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = list(CITY_DATA.keys())
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
        'saturday', 'sunday']


def verify_input(choice_list):
    """
    Verify that the user input is valid from a list of choices. Assign numbers
    to each choice so can use number for fast entry

    Arg:
        (list) choice_list - list of possible input strings
    Returns:
        (str) output - validated output
    """
    while True:
        prompt_string = f'Enter full name or number:'

        for choice in choice_list:
            choice_num = str(choice_list.index(choice)+1)
            prompt_string += f' {choice_num}) {choice.title()}'
        prompt_string += ': \n'

        response = input(prompt_string).lower()

        if response.isdigit() and int(response) <= len(choice_list):
            return choice_list[int(response)-1]
        elif response in choice_list:
            return response
        else:
            print('Invalid input. Please try again.\n')


def select_filter():
    while True:
        response = input('Would you like to filter by:\n'
                         '  1) Month (Type 1 or "Month")\n'
                         '  2) Day of week (Type 2 or "Day")\n'
                         '  3) Both month and day of week (Type 3 or "Both")\n'
                         '  4) No filter (Type 4 or "None")\n').lower()

        if response in 'none' or response == '4':
            print('Okay, no filters selected.\n')
            return 'all', 'all'
        elif response in 'both' or response == '3':
            print('Okay, please select your month and day:\n')
            return (verify_input(months), verify_input(days))
        elif response in 'month' or response == '1':
            print('Okay, please select your month only:\n')
            return (verify_input(months), 'all')
        elif response in 'day' or response == '2':
            print('Okay, please select your day only:\n')
            return ('all', verify_input(days))
        else:
            print('Invalid input. Please try again.\n')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                      month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
                    day filter
    """
    print('Hello! Let\'s explore some US bikeshare data.\n'
          'Please select the city you wish to analyse:')

    city = verify_input(cities)

    print(f'You selected {city.title()}. If this is not the'
          ' city you want, please restart.\n')

    month, day = select_filter()

    print(f'Showing you statistics for {city.title()} with the following '
          f'filter parameters: month: {month.title()}, day: {day.title()}\n')

    print('-'*40)

    return city, month, day


def most_common(df, col):
    """
    For calculating most common occurances in a specified column of a DataFrame

    Args:
        (df) df - DataFrame info
        (str) col - column to find the most common occurances
    Returns:
        count_series - Pandas series with counts of each instance
        most_common - name of the most common item
    """
    count_series = df[col].value_counts()
    most_common = count_series.idxmax()
    return count_series, most_common


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or "all" to apply no
                      month filter
        (str) day - number of the day of week to filter by, or "all" to apply
                    no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    # Reset index to delete empty rows for when viewing raw data
    df.reset_index(drop=True, inplace=True)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_counts, most_common_month = most_common(df, 'month')
    print(f'The most common month is {months[most_common_month-1].title()} '
          f'with {month_counts[most_common_month]:,d} trips.')

    # display the most common day of week
    day_counts, most_common_day = most_common(df, 'day_of_week')
    print(f'The most common day of the week is {days[most_common_day].title()}'
          f' with {day_counts[most_common_day]:,d} trips.')

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    hour_counts, most_common_hour = most_common(df, 'start_hour')
    print(f'The most common start hour is {int(most_common_hour)} hundred '
          f'with {hour_counts[most_common_hour]:,d} trips.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    s_station_counts, most_common_s_station = most_common(df, 'Start Station')
    print(f'The most common start station is {most_common_s_station} with '
          f'{s_station_counts[most_common_s_station]:,d} trips.')

    # display most commonly used end station
    e_station_counts, most_common_e_station = most_common(df, 'End Station')
    print(f'The most common end station is {most_common_e_station} with '
          f'{e_station_counts[most_common_e_station]:,d} trips.')

    # display most frequent combination of start station and end station trip
    df['Start & End Stations'] = (df['Start Station'] + ' to ' +
                                  df['End Station'])
    stations_counts, most_common_stations = most_common(df,
                                                        'Start & End Stations')
    print('The most common combination of start and end stations is '
          f'{most_common_stations} with '
          f'{stations_counts[most_common_stations]:,d} trips.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_hours = math.floor(total_travel_time / 60 / 60)
    total_travel_mins = math.floor(total_travel_time % (60*60) / 60)
    total_travel_secs = round(total_travel_time % 60)

    print(f'The total travel time is {total_travel_hours:,d} '
          f'hours, {total_travel_mins} minutes '
          f'and {total_travel_secs} seconds.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_mins = math.floor(mean_travel_time/60)
    mean_travel_secs = round(mean_travel_time % 60)

    print(f'The mean travel time is {mean_travel_mins} minutes '
          f'and {mean_travel_secs} seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of users by type:')
    print(user_types)

    # Display counts of gender
    # Check if Gender column exists as Washington data does not have such info
    if 'Gender' not in df.columns:
        print('Gender data not available for your selected filter')
    else:
        genders = df['Gender'].value_counts()
        print('Number of users by gender:')
        print(genders)

    # Display earliest, most recent, and most common year of birth
    # Check if Birth Year column exists
    if 'Birth Year' not in df.columns:
        print('Birth year data not available for your selected filter')
    else:
        earliest_birth = int(df['Birth Year'].min())
        latest_birth = int(df['Birth Year'].max())
        birth_counts, most_common_birth = most_common(df, 'Birth Year')

        print(f'The earliest birth year of users is {earliest_birth} and '
              f'the latest birth year is {latest_birth}.')
        print(f'The most common birth year is {int(most_common_birth)} with '
              f'{birth_counts[most_common_birth]:,d} trips by such users.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_raw(df):
    """ For viewing raw data 5 rows at a time """

    response = input('Do you wish to view the raw data 5 rows at a time?'
                     ' (y?) ').lower()

    if response == 'y':
        # Set option so all columns are displayed
        pd.set_option("max_columns", None)

        # Iterates 5 rows at a time and prompts user if they wants to continue
        for i in range(0, df.shape[0], 5):
            print(df.loc[i:i+4])
            proceed = input('Do you want to view the next 5 rows? '
                            '(y?) ').lower()
            if proceed != 'y':
                return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw(df)

        restart = input('\nWould you like to restart? (y?)\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
