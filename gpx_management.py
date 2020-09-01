from lxml import objectify
from geopy.distance import geodesic
import datetime
import os, fnmatch
import io


def load_file():

    try:

        cwd = os.getcwd()
        folder= "/static/gps/"
        cwd2 = cwd+folder
        for filename in os.listdir(cwd2):
            if filename.endswith(".gpx") or filename.endswith(".GPX"):
                gpxFile = cwd2+filename

                tree = objectify.parse(gpxFile)
                root = tree.getroot()
    except:
        pass

    return root



namespace = 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'
namespacetwo = 'http://www.topografix.com/GPX/1/1'


def delet_old():
    cwd = os.getcwd()
    folder= "/static/gps/"
    cwd2 = cwd+folder
    for filename in os.listdir(cwd2):
        if filename.endswith(".gpx") or filename.endswith(".GPX"):
            os.remove(cwd2+'/'+filename)

def name():
    try:
        root = load_file()

        name = root.xpath('//ns:name', namespaces={'ns': namespacetwo})

        name = str(name[0])

        name = name.replace('Running','')

        return name
    except:
        name = ''
        return name

def date():
    try:
        root = load_file()

        date = str(root.trk.trkseg.trkpt[0].time)

        startYear = date[0:4]
        startMonth = date[5:7]
        startDay = date[8:10]

        runDate= startYear+'-'+startMonth+'-'+startDay

        return runDate

    except:
        runDate = ''
        return runDate

def type():
    try:
        root = load_file()
        actType = root.xpath('//ns:type', namespaces={'ns': namespacetwo})

        text = str(actType[0])

        fullstring = text.upper()
        substring = "RUNNING"

        if substring in fullstring:
            actType='Running'

        return actType

    except:
        actType = ''

        return actType

def hr():
    try:
        root = load_file()
        hr_list = root.xpath('//ns:hr', namespaces={'ns': namespace})

        avg_len = len(hr_list)
        avg_hr=0
        for value in hr_list:
            avg_hr = avg_hr + value

        avg_hr = int((avg_hr/avg_len))
        max_hr = max(hr_list)

        return avg_hr, max_hr

    except:
        max_hr=''
        avg_hr=''
        return avg_hr, max_hr

def cadence():
    try:
        root = load_file()
        cadence_list = root.xpath('//ns:cad', namespaces={'ns': namespace})

        max_cadence = 2*(max(cadence_list))

        avg_len = len(cadence_list)
        avg_cadence = 0

        for value in cadence_list:
            avg_cadence = avg_cadence + value
        
        avg_cadence =2*(int(avg_cadence/avg_len))

        return max_cadence, avg_cadence

    except:
        max_cadence=''
        avg_cadence=''
        return max_cadence, avg_cadence

def distance():
    try:
        root = load_file()
        listLen = len(root.trk.trkseg.trkpt)-1

        totalDistance = 0

        coordinates_position = 0

        while coordinates_position < listLen:
            pos = coordinates_position
            lat1= root.trk.trkseg.trkpt[pos].attrib['lat']
            lon1= root.trk.trkseg.trkpt[pos].attrib['lon']
            lat2= root.trk.trkseg.trkpt[pos+1].attrib['lat']
            lon2= root.trk.trkseg.trkpt[pos+1].attrib['lon']
            distance = sum_coordinates(lat1, lat2, lon1, lon2)

            totalDistance = totalDistance + distance 

            coordinates_position += 1
        
        formatted_distance = f"{totalDistance:.2f}"

        formatted_distance = float(formatted_distance)

        return formatted_distance

    except:
        formatted_distance=''
        return formatted_distance


def sum_coordinates(lat1, lat2, lon1, lon2):

    pos1 = (lat1, lon1) 
    pos2 = (lat2, lon2) 
    
    result = geodesic(pos1, pos2).km

    return result

def time():
    try:
        root = load_file()
        
        timeLen = len(root.trk.trkseg.trkpt)-1

        startTime = str(root.trk.trkseg.trkpt[0].time)
        endTime = str(root.trk.trkseg.trkpt[timeLen].time)

        startYear = startTime[0:4]
        startMonth = startTime[5:7]
        startDay = startTime[8:10]
        startHour = startTime[11:13]
        startMinute = startTime[14:16]
        startSeconds = startTime[17:23]
        startAt= startYear+'-'+startMonth+'-'+startDay+' '+startHour+':'+startMinute+':'+startSeconds

        endYear = endTime[0:4]
        endMonth = endTime[5:7]
        endDay = endTime[8:10]
        endHour = endTime[11:13]
        endMinute = endTime[14:16]
        endSeconds = endTime[17:23]
        
        endAt= str(endYear)+'-'+str(endMonth)+'-'+str(endDay)+' '+str(endHour)+':'+str(endMinute)+':'+str(endSeconds)

        date_time_str2 = str(startAt)
        date_time_str = str(endAt)
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        date_time_obj2 = datetime.datetime.strptime(date_time_str2, '%Y-%m-%d %H:%M:%S.%f')

        result = date_time_obj - date_time_obj2

        return result
        
    except:
        result=''
        return result


def ele():
    try:
        root = load_file()
        
        last_elev = 0
        max_elev= 0
        min_elev= 0
        elev_diff = 0
        elev_gain = 0
        elev_los = 0
        elev_factor = 0.5
        elevLen = len(root.trk.trkseg.trkpt)-1
        first_elev	= True

        elev_position = 0

        while elev_position < elevLen:
            
            currentElev = root.trk.trkseg.trkpt[elev_position].ele

            #update max and min elevation if needed
            if currentElev > max_elev:
                max_elev = currentElev
            if currentElev < min_elev:
                min_elev = currentElev

            # If first_elev == True we don't use it, it's ou starting elevation
            if first_elev:
                last_elev = currentElev
                first_elev = False

            #Check if we gain or loss altitude

            if currentElev > last_elev:
                elev_diff = currentElev - last_elev
            if currentElev < last_elev:
                elev_diff = last_elev - currentElev

            # If elevation difference is bigger that our elev factor we sum the values

            if elev_diff >= elev_factor and currentElev > last_elev:
                elev_gain = elev_gain + elev_diff

            if elev_diff >= elev_factor and currentElev < last_elev:
                elev_los = elev_los + elev_diff
            
            last_elev= currentElev

            elev_position += 1

        split_string = str(elev_gain).split(".", 1)
        elev_gain = split_string[0]

        split_string = str(elev_los).split(".", 1)
        elev_los = split_string[0]


        return elev_gain, elev_los

    except:
        elev_gain=''
        elev_los=''
        return elev_gain, elev_los

def timeToSeconds(time):

    timeok=str(time)
    h, m, s = timeok.split(':')
    timeSeconds = int(h) * 3600 + int(m) * 60 + int(s)

    return timeSeconds

def pace(distance, time):
    try:
        resultSeconds= timeToSeconds(time)

        distanceMeters = distance*1000

        speed = ((distanceMeters) / (resultSeconds/360))/100

        distance = 1  # 1 kilometer

        seconds_speed = (distance / speed * 60)*60
        endSeconds=round(seconds_speed % 60)

        if endSeconds<10:
            endSeconds='0'+str(endSeconds)


        minutes_speed = int((seconds_speed//60))


        if minutes_speed < 10:
            minutes_speed='0'+str(minutes_speed)

        endPace= str(minutes_speed)+':'+str(endSeconds)
        
        return endPace

    except:
        endPace=''
        return endPace

def strideLenght(time, distance):
    try:
        resultSeconds= timeToSeconds(time)

        time = (resultSeconds)/60
        distanceMeters = distance * 1000
        cadence = 72
        steps = cadence * time

        stride = (distanceMeters / steps)/2

        formatted_stride = f"{stride:.2f}"

        formatted_stride = float(formatted_stride)

        return formatted_stride
    except:
        formatted_stride=''
        return formatted_stride
