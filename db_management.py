from flask import redirect, url_for
import sqlite3
import pandas as pd
import datetime
import traceback

def insert(acType, actDate, actRace, actLocation, actDistance, actCalories, actTime, actAvgHr, actMaxHr, actAvgCadence, actMaxCadence, actAvgPace, actElevGain, actElevLoss, actStrideLen):

    try:

        actTime=str(actTime)
        
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        insert_data = ('INSERT INTO activitiesTb (ActivityType, Date, Race, Title, Distance, Calories, Time, AvgHR, MaxHR, AvgCadence, MAxCadence, AvgPace, ElevGain, ElevLoss, AvgStrideLength) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        data_sql = (acType, actDate, actRace, actLocation, actDistance, actCalories, actTime, actAvgHr, actMaxHr, actAvgCadence, actMaxCadence, actAvgPace, actElevGain, actElevLoss, actStrideLen)
        cur.execute(insert_data, data_sql)
        conn.commit()
        conn.close()

    except:
        traceback.print_exc()
        return redirect(url_for('wrong'))


def update(acType, actDate, actRace, actLocation, actDistance, actCalories, actTime, actAvgHr, actMaxHr, actAvgCadence, actMaxCadence, actAvgPace, actElevGain, actElevLoss, actStrideLen):
    
    #UPDATE activitiesTb SET Calories="100" WHERE date="2020-09-07" and Distance="4.77"

    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        #sql = "UPDATE activitiesTb SET Calories = {} WHERE date = {}".format('100', '"2020-09-06"') WORKING
        sql = "UPDATE activitiesTb SET ActivityType = ?, Date= ?, Race= ?, Title= ?, Distance= ?, Calories= ?, Time= ?, AvgHR= ?, MaxHR= ?, AvgCadence= ?, MAxCadence= ?, AvgPace= ?, ElevGain= ?, ElevLoss= ?, AvgStrideLength= ? WHERE date = ?"
        update_data = (str(acType), str(actDate), str(actRace), str(actLocation), str(actDistance), str(actCalories), str(actTime), str(actAvgHr), str(actMaxHr), str(actAvgCadence), str(actMaxCadence), str(actAvgPace), str(actElevGain), str(actElevLoss), str(actStrideLen), str(actDate))


        cur.execute(update_data,sql)
        conn.commit()
        conn.close()

    except:
        traceback.print_exc()
        return redirect(url_for('wrong'))


def delete(actDate, actDistance, actTime):

    try:

        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        insert_data = ('DELETE FROM activitiesTb WHERE Date=? AND Distance=? AND Time=?')
        data_sql = (actDate, actDistance, actTime)
        cur.execute(insert_data, data_sql)

        conn.commit()
        conn.close()

    except:
        return redirect(url_for('wrong'))

def view():
    
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        cur.execute('SELECT * FROM activitiesTb ORDER BY Date DESC LIMIT 100')
        result=cur.fetchall()
        conn.close()
        return result

    except:
        return redirect(url_for('wrong'))

def viewAll():
    
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        cur.execute('SELECT * FROM activitiesTb ORDER BY Date DESC')
        result=cur.fetchall()
        conn.close()
        return result

    except:
        return redirect(url_for('wrong'))


def view_details(date, distance):

    try:
        date=date
        distance=distance
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()


        split_string = str(distance).split(".", 1)
        distance = split_string[0]
        
        date = str(date)+'%'
        distance=str(distance)+'%'

        query_string = 'SELECT * FROM activitiesTb WHERE date LIKE ? AND Distance LIKE ?'
        cur.execute(query_string, (date, distance))

        result=cur.fetchone()
        conn.close()
        return result
    except:
        return redirect(url_for('wrong'))

def find_duplicates(date, distance):
    try:
        result=False
        date=date
        distance=distance
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()


        split_string = str(distance).split(".", 1)
        distance = split_string[0]
        
        date = str(date)+'%'
        distance=str(distance)+'%'

        query_string = 'SELECT * FROM activitiesTb WHERE date LIKE ? AND Distance LIKE ?'
        cur.execute(query_string, (date, distance))

        result=cur.fetchone()
        conn.close()

        if result != None:
            result = True
        else:
            result=False


        return result
    
    except:
        return redirect(url_for('wrong'))


def countActivities():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        cur.execute('SELECT count(*) from activitiesTb')
        resultCount=cur.fetchone()
        conn.close()
        return resultCount

    except:
        return redirect(url_for('wrong'))

def getLongest():

    try:
        conn=sqlite3.connect("runningLog.sqlite")
        curMax=conn.cursor()
        curMax.execute('SELECT MAX(Distance), Date FROM activitiesTb')
        resultMax=curMax.fetchone()
        conn.close()
        return resultMax
    except:
        return redirect(url_for('wrong'))


def getTotalDistance():

    try:
        conn=sqlite3.connect("runningLog.sqlite")
        curDist=conn.cursor()
        curDist.execute('SELECT SUM(Distance) from activitiesTb')
        resultTotalDist=curDist.fetchone()
        conn.close()
        return resultTotalDist

    except:
        return redirect(url_for('wrong'))


def getTotalElev():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        curElev=conn.cursor()
        curElev.execute('SELECT SUM(ElevGain) from activitiesTb')
        resultTotalElev=curElev.fetchone()
        conn.close()
        return resultTotalElev

    except:
        return redirect(url_for('wrong'))

def getMaxElev():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        curMaxElev=conn.cursor()
        curMaxElev.execute('SELECT MAX(ElevGain), Date from activitiesTb')
        resultMaxElev=curMaxElev.fetchone()
        conn.close()
        return resultMaxElev

    except:
        return redirect(url_for('wrong'))


def getTotalHours():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        curHours=conn.cursor()
        curHours.execute('SELECT SUM(Time) from activitiesTb')
        resultTotalHours=curHours.fetchone()
        conn.close()
        return resultTotalHours

    except:
        return redirect(url_for('wrong'))

def getMaxHr():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        curMaxHr=conn.cursor()
        curMaxHr.execute('SELECT MAX(MaxHr) from activitiesTb')
        resultMaxHr=curMaxHr.fetchone()
        conn.close()
        return resultMaxHr

    except:
        return redirect(url_for('wrong'))


def getAvgHr():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        curAvgHr=conn.cursor()
        curAvgHr.execute('SELECT ROUND(AVG(AvgHr)) from activitiesTb WHERE AvgHr!=0')
        resultAvgHr=curAvgHr.fetchone()
        conn.close()
        return resultAvgHr

    except:
        return redirect(url_for('wrong'))

def getBestYear():
    try:
        conn=sqlite3.connect("runningLog.sqlite")

        df= pd.read_sql_query('select ROUND(SUM(Distance)) as Kms, strftime(\"%Y\", Date) as \'year\' from activitiesTb group by strftime(\"%Y\", Date);', conn)
        maxim=df.max()

        maxYeardf = df.loc[df['Kms']==maxim[0]]

        resultBestKm=maxim[0]
        resultBestYear= maxYeardf.year

        return resultBestYear, resultBestKm

    except:
        return redirect(url_for('wrong'))

def getBestMonth():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()

        cur.execute('select SUM(Distance) as Kms, strftime(\"%m-%Y\", Date) as \'date\' from activitiesTb group by strftime(\"%m-%Y\", Date) ORDER By kms DESC LIMIT 1;')
        result=cur.fetchone()
        conn.close()

        return result

    except:
        return redirect(url_for('wrong'))

def getUsualLocation():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()

        cur.execute('SELECT COUNT(Title) as location, Title FROM activitiesTb GROUP BY Title ORDER BY location DESC LIMIT 1')
        result=cur.fetchone()
        conn.close()

        return result

    except:
        return redirect(url_for('wrong'))

def getLocation():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        cur.execute('SELECT COUNT(Title) as location, Title FROM activitiesTb GROUP BY Title ORDER BY location DESC')
        result=cur.fetchall()
        conn.close()
        return result

    except:
        return redirect(url_for('wrong'))

def getRaces():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        cur.execute('SELECT * FROM activitiesTb WHERE Race=1 ORDER BY Date DESC')
        result=cur.fetchall()
        conn.close()
        return result
    except:
        return redirect(url_for('wrong'))

def getBestResult(distanceStart,distanceEnd):
    try:
        distanceStart=distanceStart
        distanceEnd=distanceEnd

        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        query_string =('SELECT * FROM activitiesTb WHERE Race=1 AND Distance>? and Distance<? ORDER By (Time)ASC LIMIT 1')

        cur.execute(query_string, (distanceStart, distanceEnd))
        result=cur.fetchone()
        conn.close()

        return result

    except:
        return redirect(url_for('wrong'))

def getYears():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        cur.execute('select strftime(\"%Y\", Date) as \'year\' from activitiesTb group by strftime(\"%Y\", Date)')
        result=cur.fetchall()
        conn.close()
        return result

    except:
        return redirect(url_for('wrong'))

def getKmsTodayByYear():

    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        
        years = getYears()

        yearList=[]
        kmsList=[]

        for year in years:
            
            now = datetime.datetime.now()
            day=str(now.day)
            month=str(now.month)

            dayQuery=""
            monthQuery=""

            if int(now.day) < 10:
                dayQuery="0"+str(day)
            else:
                dayQuery=str(now.day)

            if int(now.month) < 10:
                monthQuery="0"+str(month)
            else:
                monthQuery=str(now.month)


            yearStr=str(year)
            yearQuery=yearStr[2:6]
            
            toDate=str(yearQuery)+'-'+str(monthQuery)+'-'+str(dayQuery)
            fromDate=str(yearQuery)+'-'+'01-01'

            fromD=str(fromDate)
            toD=str(toDate)

            yearList.append(str(year))
            
            cur.execute('SELECT ROUND(SUM(Distance)) from activitiesTb where Date BETWEEN ? AND ?',(fromD,toD))
            result=cur.fetchone()

            kmsList.append(result)

        return kmsList
        
    except:
        return redirect(url_for('wrong'))

def getLastActivityDate():
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()
        cur.execute('select Date from activitiesTb ORDER BY date DESC LIMIT 1')
        result=cur.fetchone()
        conn.close()
        return result

    except:
        return redirect(url_for('wrong'))

def stravaStatus():
        
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()

        cur.execute('SELECT * FROM config WHERE name="client"')
        result=cur.fetchone()
        conn.close()
        
        return result

    except:
        return redirect(url_for('wrong'))


def setStravaConf(client, secret):
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()

        #first we make sure we don't have any old data for Strava conf

        cur.execute('SELECT * FROM config WHERE name="secret"')
        resultSecret=cur.fetchone()

        if resultSecret is None:
            pass
        else:
            cur.execute('DELETE FROM config WHERE name="secret"')
            conn.commit()  
            conn.close()

        cur.execute('SELECT * FROM config WHERE name="client"')
        resultClient=cur.fetchone()

        if resultClient is None:
            pass
        else:
            cur.execute('DELETE FROM config WHERE name="client"')
            conn.commit()  
            conn.close()

        #now we insert new Strava conf

        insert_data = ('INSERT INTO config (name, value) VALUES (?, ?)')
        data_sql = ('client',client)
        cur.execute(insert_data, data_sql)
        conn.commit()  
        insert_data = ('INSERT INTO config (name, value) VALUES (?, ?)')
        data_sql = ('secret',secret)
        cur.execute(insert_data, data_sql)
        conn.commit()  
        
        conn.close()


    except:
        return redirect(url_for('wrong'))    


def stravaConf():
    
    try:
        conn=sqlite3.connect("runningLog.sqlite")
        cur=conn.cursor()

        cur.execute('SELECT * FROM config')
        result=cur.fetchall()
        conn.close()

        config = pd.DataFrame(result)

        config.columns = ['name','value']#set colum names

        config.set_index('name', inplace=True)#set index by colum value

        return config

    except:
        return redirect(url_for('wrong'))