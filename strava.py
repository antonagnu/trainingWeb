import pandas as pd
import requests
import json
import time
import datetime
import db_management as db_management


def getLastDate():
    
    lastDate = db_management.getLastActivityDate()
    lastDateOk = str(lastDate[0])

    unixDate = time.mktime(datetime.datetime.strptime(lastDateOk, "%Y-%m-%d").timetuple())

    return unixDate


def connectStrava(tokenStrava):



    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': 44164,
                                'client_secret': '1cef63bfc5b7cf6a96e6ffab48e8fdbeafd008aa',
                                'code': tokenStrava,
                                'grant_type': 'authorization_code'
                                }
                    )#Save json response as a variable
    strava_tokens = response.json()# Save tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)# Create json file with Token 


def getActivities():

    unixDate = getLastDate()

    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)# Loop through all activities
    page = 1
    url = "https://www.strava.com/api/v3/athlete/activities"
    access_token = strava_tokens['access_token']# Create the dataframe ready for the API call to store your activity data
    activities = pd.DataFrame(
        columns = [
                "id",
                "name",
                "start_date_local",
                "type",
                "distance",
                "moving_time",
                "start_latlng",
                "total_elevation_gain",
                "end_latlng",
                "external_id"
        ]
    )
    while True:
        # get page of activities from Strava
        #r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&after=1597705200.0' + '&page=' + str(page))
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&after=' + str(unixDate) + '&page=' + str(page))
        r = r.json()

        # if no results exit loop
        if (not r):
            break
        
        # add new data to dataframe
        for x in range(len(r)):
            activities.loc[x + (page-1)*200,'id'] = r[x]['id']
            activities.loc[x + (page-1)*200,'name'] = r[x]['name']
            activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
            activities.loc[x + (page-1)*200,'type'] = r[x]['type']
            activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
            activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
            activities.loc[x + (page-1)*200,'start_latlng'] = r[x]['start_latlng']
            activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
            activities.loc[x + (page-1)*200,'end_latlng'] = r[x]['end_latlng']
            activities.loc[x + (page-1)*200,'external_id'] = r[x]['external_id']    
        page += 1

        activitiesRun = activities.loc[activities['type'] == 'Run']

    return activitiesRun