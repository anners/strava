# this is a script to print out strava activites after a certain date 
# I created this for a work running challenge b/c I didn't want to manually update a spreadsheet 
# this was heavily influnced by the work Matt Ambrogi https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde
import os
import numpy as np
import requests
import urllib3
from datetime import datetime, timedelta
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token(client_id, client_secret):
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': "312931ab27c4904e31222fc3c4bcb71c9e865736",
        'grant_type': "refresh_token",
        'f': 'json'
    }

    #print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    #print("Access Token = {}\n".format(access_token))
    return access_token

def get_strava_activities(access_token):
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    
    #convert dataset to pandas
    activities = pd.json_normalize(my_dataset)
    return activities

def update_activity_table(activities):
    # restricted to the columns we care about 
    cols = ['name', 'type', 'distance', 'moving_time', 'total_elevation_gain', 'start_date_local' ]
    activities = activities[cols]

    #Break date into start time and date
    activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
    activities['start_time'] = activities['start_date_local'].dt.time
    activities['start_date_local'] = activities['start_date_local'].dt.date

    #convert meters to miles 
    activities['distance'] = (activities['distance'] / 1609)
    activities['distance'] = np.trunc(100 * activities['distance']) / 100 

    #convert meters to feet
    activities['total_elevation_gain'] = (activities['total_elevation_gain'] * 3.281)
    activities['total_elevation_gain'] = np.trunc(100 * activities['total_elevation_gain']) / 100

    #convert seconds to hours
    activities['moving_time'] = pd.to_datetime(activities['moving_time'], unit="s").dt.strftime("%H:%M:%S")

    return activities

def get_recent_activites(activities, start_date): 
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() 
    activities['recent'] = np.where(activities['start_date_local'] > start_date, 'true', 'false')
    #print(activities['recent'])

    return activities.loc[activities['recent'] == 'true']
    

def main (): 
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    access_token = get_access_token(client_id, client_secret)

    activities = get_strava_activities(access_token)

    activities = update_activity_table(activities)

    #start_date = '2023-11-01'
    recent_activities = get_recent_activites(activities, '2023-11-01')

    print(recent_activities.iloc[:,:-1])
    #recent_activities.to_csv('out.csv')


if __name__ == "__main__":
    main()