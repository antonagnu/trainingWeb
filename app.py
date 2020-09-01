from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import AddForm
import db_management
import plot_management as plot
import gpx_management
import strava
import time
import os

app=Flask(__name__)

app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY'] = 'mysecretkey'
app.config["FILE_UPLOADS"] = "./static/gps"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/view_data')
def view_data():

    return render_template("view_data.html", results=db_management.view())

@app.route('/overview', methods=("POST", "GET"))
def overview():
    actCount=db_management.countActivities()
    longest= db_management.getLongest()
    totalDist=db_management.getTotalDistance()
    totalElev=db_management.getTotalElev()
    maxElev=db_management.getMaxElev()
    totalHours=db_management.getTotalHours()
    maxHr=db_management.getMaxHr()
    avgHr=db_management.getAvgHr()
    bestYear=db_management.getBestYear()
    bestMonth=db_management.getBestMonth()
    bestYearDistance=bestYear[1]
    bestYearDate=int(bestYear[0])
    usualLocation=db_management.getUsualLocation()


    return render_template("overview.html",usualLocation=usualLocation,bestMonth=bestMonth,  bestYearDistance=bestYearDistance, bestYearDate=bestYearDate,actCount=actCount , longest=longest, totalDist=totalDist, totalElev=totalElev, maxElev=maxElev, totalHours=totalHours, avgHr=avgHr, maxHr=maxHr)       


@app.route('/insert_data_options')
def insert_options():

    return render_template("insert_data.html")

@app.route('/wrong')
def wrong():

    return render_template("wrong.html")

@app.route('/insert_data', methods=("POST", "GET"))
def insert_data():
    form = AddForm()
 
    if form.validate_on_submit():
        
        Type = "Running"
        Date = form.date.data
        Race = form.race.data
        Location = form.location.data
        Distance = form.distance.data
        Calories = '0'
        Time = form.time.data
        AvgHr = form.avgHr.data
        MaxHr = form.maxHr.data
        AvgCadence = form.avgCadence.data
        MaxCadence = form.maxCadence.data
        AvgPace = form.avgPace.data
        ElevGain = form.elevGain.data
        ElevLoss = form.elevLoss.data
        StrideLen = form.avgStrideLength.data


        db_management.insert(Type, Date, Race, Location, Distance, Calories, Time, AvgHr, MaxHr, AvgCadence, MaxCadence, AvgPace, ElevGain, ElevLoss, StrideLen)
       
        return render_template('home.html')

    return render_template("insert_manually.html", form=form)    


@app.route('/graph')
def graph_data():

    time.sleep(1)

    return render_template('graph.html', result=plot.create_graph())

@app.route('/details', methods=("POST", "GET"))
def details():

    date = request.args.get('date')
    dist = request.args.get('dist')

    return render_template("view_details.html", results=db_management.view_details(date,dist))

@app.route('/delete', methods=("POST", "GET"))
def delete():

    actDate = request.args.get('actDate')
    actDistance = request.args.get('actDistance')
    actTime = request.args.get('actTime')

    db_management.delete(actDate,actDistance,actTime)
    db_management.view()

    return render_template("view_data.html", results=db_management.view())



@app.route('/races', methods=("POST", "GET"))
def races():
    
    return render_template("races.html", races=db_management.getRaces(), half=db_management.getBestResult(20.5,22),ten=db_management.getBestResult(9.8, 11), marathon=db_management.getBestResult(41.9,43))


@app.route('/today', methods=("POST", "GET"))
def today():
    kmsList=db_management.getKmsTodayByYear()
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

    yearList=db_management.getYears()
    yearsInt=[]
    x = 0
    endList= len(yearList)
    while x < endList:
        yearInt=yearList[x][0]
        yearsInt.append(int(yearInt))
        x += 1
    
    kmPosition=(kmsIntList.index(max(kmsIntList)))
    yearBest=yearsInt[kmPosition]

    nowKms=kmsIntList[len(yearList)-1]
    
    if nowKms >= max(kmsIntList):
        doingGreat=True
    else:
        doingGreat=False

    return render_template("today.html", kmsToday=max(kmsIntList), years=yearBest, doingGreat=doingGreat, nowKms=nowKms)


@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":

        if request.files:

            file = request.files["file"]

            file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))

            return redirect(url_for('gps'))

    return render_template("insert_from_file.html")


@app.route('/gps', methods=("POST", "GET"))
def gps():

    Race = '0'
    Calories = '0'
    Location = gpx_management.name()
    hr_values = gpx_management.hr()
    AvgHr = int(hr_values[0])
    MaxHr =  int(hr_values[1])
    Distance = gpx_management.distance()
    Type = gpx_management.type()
    Time = str(gpx_management.time())
    cadence = gpx_management.cadence()
    AvgCadence = cadence[1]
    MaxCadence = cadence[0]
    elev = gpx_management.ele()
    ElevGain = elev[0]
    ElevLoss = elev[1]
    AvgPace = gpx_management.pace(Distance,Time)
    Date = gpx_management.date()
    StrideLen = gpx_management.strideLenght(Time, Distance)
    duplicate = db_management.find_duplicates(Date,Distance)

    if request.args.get('insert') == 'Insert':
     
        db_management.insert(Type, Date, Race, Location, Distance, Calories, Time, AvgHr, MaxHr, AvgCadence, MaxCadence, AvgPace, ElevGain, ElevLoss, StrideLen)
        gpx_management.delet_old()
        return render_template('home.html')

    else:

        return render_template("gps.html", duplicate=duplicate, date=Date, name=Location, hr_values=hr_values, distance=Distance, acttype=Type, time=Time, elev=elev, cadence=cadence, pace=AvgPace, stride=StrideLen)


@app.route('/exchange_token')
def exchange_token():

    token = request.args.get('code')
    
    strava.connectStrava(token)

    activityList = strava.getActivities()

    return render_template("strava.html", activityList=activityList)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
