from flask import redirect, url_for
import pandas as pd
import requests
import json
import time
import datetime
import math
from geopy.geocoders import Nominatim
import db_management as db_management


def pace(time, distance):

    try:
        
        speed = ((distance) / (time/360))/100

        dist = 1  # 1 kilometer

        seconds_speed = (dist / speed * 60)*60
        endSeconds=round(seconds_speed % 60)

        if endSeconds<10:
            endSeconds='0'+str(endSeconds)

        minutes_speed = int((seconds_speed//60))

        if minutes_speed < 10:
            minutes_speed='0'+str(minutes_speed)

        endPace= str(minutes_speed)+':'+str(endSeconds)

        return endPace
    except:
        return redirect(url_for('wrong'))

def getLastDate():
    try:
        #get date for the last activity stored in the data base
        lastDate = db_management.getLastActivityDate()
        lastDateOk = str(lastDate[0])

        unixDate = time.mktime(datetime.datetime.strptime(lastDateOk, "%Y-%m-%d").timetuple())#convert date to unix format to be use in Strava API

        return unixDate
    except:
        return redirect(url_for('wrong'))

def connectStrava(tokenStrava):

    try:

        stravaConf = db_management.stravaConf()

        client = stravaConf.loc[ 'client' , : ]
        secret = stravaConf.loc[ 'secret' , : ]

        client = str(client[0])
        secret = str(secret[0])

        response = requests.post(
                            url = 'https://www.strava.com/oauth/token',
                            data = {
                                    'client_id': client,
                                    'client_secret': secret,
                                    'code': tokenStrava,
                                    'grant_type': 'authorization_code'
                                    }
                        )#Save json response as a variable
        strava_tokens = response.json()# Save tokens to file
        with open('strava_tokens.json', 'w') as outfile:
            json.dump(strava_tokens, outfile)# Create json file with Token 
    except:
        return redirect(url_for('wrong'))


def getActivities():

    try:

        unixDate = getLastDate()

        with open('strava_tokens.json') as json_file:
            strava_tokens = json.load(json_file)# Loop through all activities
        page = 1
        url = "https://www.strava.com/api/v3/athlete/activities"
        access_token = strava_tokens['access_token']# Create the dataframe ready for the API call to store your activity data

        # get page of activities from Strava
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&after=' + str(unixDate) + '&page=' + str(page))
        r = r.json()

        col = ['distance','moving_time','total_elevation_gain','type','start_date','average_speed','average_cadence','average_heartrate','max_heartrate','start_latlng']

        total = len(r)
        length = len(col) 

        i = 0
        z = 0

        newData=[]

        while i < total:
            act = r[i]
            actT = act['type']
            
            if actT == 'Run':

                z = 0

                while z < length:
                    colCheck = col[z]

                    if act.get(colCheck) is not None:
                        pass
                    else:
                        act.update({ colCheck : 0 })
    
                    z +=1
                newData.append(act)
            
            else:
                pass

            i += 1

        activitiesRun = pd.DataFrame(newData)
     

        columns = activitiesRun[['distance','moving_time','total_elevation_gain','type','start_date','average_speed','average_cadence','average_heartrate','max_heartrate','start_latlng']]

        activitiesFiltered = columns.copy()

        activitiesFilteredOk = formatActivities(activitiesFiltered)


        return activitiesFilteredOk

    except:
        return redirect(url_for('wrong'))

def formatActivities(df):

    try:

        pandLen = len(df)

        formattedData = pd.DataFrame(columns=['distance','moving_time','total_elevation_gain','type','start_date','average_speed','average_cadence','average_heartrate','max_heartrate','start_latlng'])

        i = 0
        while i < pandLen:

            newData = df.iloc[i]
            #Format time
            try:
                timeOrg = int(newData['moving_time'])
                timeOk = str(datetime.timedelta(seconds=timeOrg))
                newData.at['moving_time']= timeOk
            except:
                newData.at['moving_time']=0
            #Format type
            try:
                newData.at['type']= 'Running'
            except:
                newData.at['type']=''

            #Format distance
            try:
                distOrg = newData['distance']
                distanceOk = str(distOrg /1000)
                distanceOk=distanceOk[0:4]
                newData.at['distance']= distanceOk
            except:
                newData.at['distance']= 0
            #Format Cadence
            try:
                cadenOrg = newData['average_cadence']
                cadenOk = math.trunc(cadenOrg)
                newData.at['average_cadence'] = cadenOk*2
            except:
                newData.at['average_cadence'] =0
            #Format MaxHr
            try:
                maxHrOrg = int(newData['max_heartrate'])
                maxHrOk = math.trunc(maxHrOrg)
                newData.at['max_heartrate'] = maxHrOk
            except:
                newData.at['max_heartrate'] =0
            #Format Avg.Hr
            try:
                avgHrOrg = int(newData['average_heartrate'])
                avgHrOk = math.trunc(avgHrOrg)
                newData.at['average_heartrate'] = avgHrOk
            except:
                newData.at['average_heartrate'] =0
            #Format Date
            try:
                dateOrg = newData['start_date']
                dateOk = dateOrg[0:10]
                newData.at['start_date'] = dateOk
            except:
                newData.at['start_date'] = 0
            #Format Pace
            try:
                paceOk = pace(timeOrg, distOrg)
                paceOk = paceOk[0:5]
                newData.at['average_speed'] = paceOk
            except:
                newData.at['average_speed'] = 0
            #Format location
            try:
                location=newData['start_latlng']
                lat=location[0]
                lon=location[1]
                coordinates = str(lat) + ',' + str(lon)
                locOk = getLocation(coordinates)
                newData.at['start_latlng'] = locOk
            except:
                newData.at['start_latlng']='Planet Earth'

            if db_management.find_duplicates(dateOk, distanceOk):
                # if the record already exist we don't add it to the dataframe
                pass
            else:
                #new records get added to the dataframe
                dictData = newData.to_dict()
                formattedData = formattedData.append(dictData, ignore_index=True)

            i += 1

        return formattedData

    except:
        return redirect(url_for('wrong'))


def bulkInsert(data):

    try:

        dataLen = len(data)

        i = 0
        while i < dataLen:
            result = data.iloc[i]

            Type = 'Running'
            Date= str(result['start_date'])
            Distance = str(result['distance'])
            Time= str(result['moving_time'])
            AvgHr= str(result['average_heartrate'])
            MaxHr= str(result['max_heartrate'])
            AvgCadence= str(result['average_cadence'])
            AvgPace= str(result['average_speed'])
            ElevGain= str(result['total_elevation_gain'])
            Calories=0
            MaxCadence = 0
            ElevLoss = 0
            StrideLen=0
            Race = 0
            Location = str(result['start_latlng'])

            db_management.insert(Type, Date, Race, Location, Distance, Calories, Time, AvgHr, MaxHr, AvgCadence, MaxCadence, AvgPace, ElevGain, ElevLoss, StrideLen)    
    
            i += 1
    except:
        return redirect(url_for('wrong'))

def getLocation(coordinates):

    try:

        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse(str(coordinates))
        location = location.address
        result = location.split(',')
        result = result[-5]

        return result
    except:
        return redirect(url_for('wrong'))