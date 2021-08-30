
import time
import pandas as pd
import numpy as np

#from pandasql import sqldf
#pysqldf=lambda q: sqldf(q,globals())

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#define month array
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
#define week day array
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

TIME_FILTERS=['month', 'day', 'both', 'none']

TIME_FILTERS_LIB={'month': ['january', 'february', 'march', 'april', 'may', 'june'],
              'day':  ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
              'both':[],
              'none':[]}

def _to_list_string(l):
    #convert list values to string
    l = [word.capitalize() for word in l]
    if len(l) <= 1:
        return ''.join(l)

    return ','.join(l[:-1]) + ', or {}'.format(l[-1])


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
    city=input('Would you like to see data for {}? '.format(_to_list_string(CITY_DATA.keys()))).lower()


    while not city in CITY_DATA.keys() or not city or city=='no':
        if city=='no':
            print('Exiting the program. please restart the program to see the data for {}.'.format(_to_list_string(CITY_DATA.keys()).title()))
            exit()
        elif city=='yes':
            city= input('Please select a city from {}:'.format(_to_list_string(CITY_DATA.keys()))).lower()
        else:
            city= input('Sorry, there is no data for {}. Please select a city from {}:'.format(city.title(),_to_list_string(CITY_DATA.keys()))).lower()




    month_day=input('Would you like to filter the data by {}? '.format(_to_list_string(TIME_FILTERS))).lower()
    while not month_day in TIME_FILTERS:
        month_day=input('Please select a filter option - {}: '.format(_to_list_string(TIME_FILTERS))).lower()

    month=''
    day=''
    if month_day.lower() == 'month':
    # TO DO: get user input for month (all, january, february, ... , june)
        month=input('Which month - {}? '.format(_to_list_string(MONTHS))).lower()
        while not month in MONTHS:
            month=input('Please select from the follwing months- {}: '.format(_to_list_string(MONTHS))).lower()
        day='all'
    elif month_day.lower()=='day':
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        month='all'
        day=input('Which day - {}? '.format(_to_list_string(DAYS))).lower()
        while not day in DAYS:
            day=input('Please enter- {}: '.format(_to_list_string(DAYS))).lower()
    elif month_day.lower()=='both':
        while not month in MONTHS:
            month=input('Which month - {}? '.format(_to_list_string(MONTHS))).lower()
        while not day in DAYS:
            day=input('Which day - {}? '.format(_to_list_string(DAYS))).lower()
    else:
        month='all'
        day='all'

    print('-'*40)
    #print(city, month, day)
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
    df['year'] = df['Start Time'].dt.year
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    week_days=list(df['day_of_week'].dropna().unique())

    if month in MONTHS and day.title() in week_days:
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df.loc[(df['month'] == month) & (df['day_of_week'] == day.title())]

    elif month in MONTHS and day.title() not in week_days:
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    elif month not in MONTHS and day.title() in week_days:
        # filter by day of week to create the new dataframe
        df=df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
# convert the Start Time column to datet    df['Start Time'] = pd.to_datetime(df['Start T])

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # TO DO: display the most common month
    popular_month=df['month'].mode()[0]
    popular_month_list=df['month'].value_counts()[:1]
    if df['month'].nunique()>1:
        print('The most popular start month and counts:')
        print(popular_month_list)
    else:
        print('Travel information of month {}. '.format(popular_month))

    # TO DO: display the most common day of week
    popular_day=df['day_of_week'].mode()[0]
    popular_day_list=df['day_of_week'].value_counts()[:1]
    if df['day_of_week'].nunique()>1:
        print('The most popular start day and counts: ')
        print(popular_day_list)
    else:
        print('Travel information of {}.'.format(popular_day))


    # TO DO: display the most common start hour

    # extract hour from the Start Time column to create an  column
    df['hour'] = df['Start Time'].dt.hour
    #print(df)
    # find thst popular hour
    #popular_hour=df['hour'].mode()[0]
    popular_hour_list=df['hour'].value_counts()[:3]
    print('The most popular start hours and counts:')
    print(popular_hour_list)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_st=df['Start Station'].mode()[0]

    print('Most Commonly Used Start Station:', popular_start_st)


    # TO DO: display most commonly used end station
    popular_end_st=df['End Station'].mode()[0]

    print('Most Commonly Used End Station:', popular_end_st)


    # TO DO: display most frequent combination of start station and end station trip
    df['start_end']=df['Start Station']+' to '+df['End Station']
    #print(df)
    popular_comb=df['start_end'].mode()[0]
    print('Most Frequent Combination of Start Station and End Station Trip: Start from', popular_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration=df['Trip Duration'].sum()
    print('Total Travel Time in Seconds: {}.'.format(total_duration))

    # TO DO: display mean travel time
    mean_duration=df['Trip Duration'].mean()
    print('Mean Travel Time in Seconds: {}.'.format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_ct=df['User Type'].nunique()
    #user_types=df['User Type'].dropna().unique()
    user_list=df['User Type'].value_counts(ascending=True)
    #user_type=''
    #for i in range(len(user_types)):
    #    user_type=user_type+user_types[i]+', '
    print('{} User Types and Counts: '.format(user_type_ct))
    print(user_list)
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_ct=df['Gender'].nunique()
        #gender_types=df['Gender'].dropna().unique()
        gender_list=df['Gender'].value_counts(ascending=True)
        #gender_str=''
        #for i in range(len(gender_types)):
        #    gender_str=gender_str+gender_types[i]+', '
        print('{} Genders and Counts:'.format(gender_ct))
        print(gender_list)
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        e_year=df['Birth Year'].min()
        r_year=df['Birth Year'].max()
        c_year=df['Birth Year'].mode()[0]
        print('The earliest year of birth is {}. The most recent year of birth is {}. The most common year of birth is {}. '.format(int(e_year),int(r_year),int(c_year)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_detail(df):
    """Displays trip detail on bikeshare users."""
    i=0
    while True:
        f_detail=input('\nWould you like to see more trip details? Enter yes or no.\n')
        if f_detail.lower()=='yes':
            start_time = time.time()
            print('\nTrip details...\n')
            #print(df.head(n=5).to_string(index=False))
            for i in range(i,i+5):
                print(df.iloc[i])
            i+=5
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)
        elif f_detail.lower()=='no':
            break
        else:
            continue


    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        #print(city,month,day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_detail(df)

        restart=''
        while restart !='yes' or restart !='no':
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()

            if restart == 'no':
                exit()
            elif restart == 'yes':
                break




if __name__ == "__main__":
	main()
