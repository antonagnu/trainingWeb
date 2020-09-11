from flask import render_template
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
import io
import db_management
import datetime


def delete_old():

    try:
        cwd = os.getcwd()
        folder= "/static/graph/"
        cwd2 = cwd+folder
        for filename in os.listdir(cwd2):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                os.remove(cwd2+'/'+filename)
    except:
        return render_template("wrong.html")


def create_graph():

    try:

        delete_old()
        conn=sqlite3.connect("runningLog.sqlite")
        
        #create the Yearly Kms graph
        df= pd.read_sql_query('select SUM(Distance) as Kms, strftime(\"%Y\", Date) as \'year\' from activitiesTb group by strftime(\"%Y\", Date);', conn)

        df.plot(kind='bar',x='year',y='Kms',color='blue', legend=True)

        plt.savefig('./static/graph/kms.png')

        #create the AvgPace graph

        df= pd.read_sql_query('select SUM(ElevGain) as ElevGain, strftime(\"%Y\", Date) as \'year\' from activitiesTb group by strftime(\"%Y\", Date);', conn)

        
        df.plot(kind='bar',x='year',y='ElevGain',color='green', legend=True)

        plt.savefig('./static/graph/elev.png')

        #create the up to today Kms graph

        kmsList=db_management.getKmsTodayByYear()
        yearList=db_management.getYears()

        yearsInt=[]
        x = 0
        endList= len(yearList)
        while x < endList:
            yearInt=yearList[x][0]
            yearsInt.append(int(yearInt))
            x += 1
        
        kmsIntList=[]
        y=0
        endKmList=len(kmsList)

        while y < endKmList:
            kmsInt=kmsList[y][0]
            if not (kmsInt is None):
                kmsIntList.append(kmsInt)
            else: 
                kmsIntList.append(0)
            y += 1

        df2 = pd.DataFrame(list(zip(kmsIntList, yearsInt)), columns =['kms', 'years']) 

        df2.plot(kind='bar',x='years',y='kms',color='red', legend=True)

        plt.savefig('./static/graph/kmsToday.png')
    
    except:

        return render_template("wrong.html")
