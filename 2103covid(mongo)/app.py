import datetime
from dateutil import parser
import sys
from flask import Flask, render_template, url_for
from flask import request, jsonify
import mysql.connector
import pymongo

app = Flask(__name__)

# mongodb
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
# db
mydb = client['CovidSEA']
# collections
mycol = mydb['vaccination']
mycol1 = mydb['worldindata']
app = Flask('2103proj')

# 1st , any mongodb query will be declared through this statement '
# this query is finding an iso_code where is labelled as "BRN"
# myquery = { "group": "BRN"}


# 2nd store the query using mycol which links to your collection and store in variable mydoc.
# for this , you if its . find means find everything in collection you can replace it with
# insertmany , insert one depending on the mongo query you need.

# query 11 aggregate always use this format
personfullyvaccinated = mycol.aggregate([{
    "$group":
        {"_id": "",
         "SUM": {"$sum": '$PERSONS_FULLY_VACCINATED'}
         }}
])

# query 2
totalnumberofcasestodate = mycol1.aggregate(
    [{"$group":
          {"_id": '$location',
           "Total_cases": {"$max": '$total_cases'}, "data": {"$last": '$date'}

           }

      }])

# query 10
totalvaccineSEA = mycol.find({}, {"_id": 0, "COUNTRY": 1, "PERSONS_FULLY_VACCINATED": 1})

# query 8
percentagetotaldeath = mycol1.aggregate(
    [{"$group":
          {"_id": '$location',
           "Total_Cases": {"$last": '$total_cases'},
           "Total Deaths": {"$last": "$total_deaths"},
           "Latest Date": {"$last": "$date"}

           }

      }])

# query 9
casesanddeathwithinpopulation = mycol1.aggregate([{"$group":
                                                       {"_id": '$location',
                                                        "Total Cases": {"$last": '$total_cases'},
                                                        "Total Deaths": {"$last": "$total_deaths"},
                                                        "Population": {"$max": "$population"},
                                                        "Date": {"$last": "$date"}

                                                        }

                                                   }])

# query 6
totalcase = mycol1.aggregate(
    [{
        "$group": {"_id": "$location", "total": {"$last": "$total_cases"}}},
        {"$group": {"_id": "null", "TotalCase": {"$sum": "$total"}}}])


# displays fifth page
@app.route("/fifthpage")
def fifthpage():
    dailyhosp = mycol1.find({}, {"_id": 0, "location": 1, "date": 1, "hosp_patients": 1, "new_cases": 1});

    # Covid-19 Cases for each SEA country to date
    ICUDates = list()
    SingaporeICUDict = {}
    BruneiICUDict = {}
    MyanmarICUDict = {}
    MalaysiaICUDict = {}
    CambodiaICUDict = {}
    PhillipinesICUDict = {}
    VietnamICUDict = {}
    TimorICUDict = {}
    ThailandICUDict = {}
    LaosICUDict = {}
    IndonesiaICUDict = {}
    SEAICUDict = {}
    WeeklyVal = list()
    SEAWeeklyVal = {}
    SingaporeWeeklyVal = {}
    BruneiWeeklyVal = {}
    MyanmarWeeklyVal = {}
    MalaysiaWeeklyVal = {}
    CambodiaWeeklyVal = {}
    PhilippinesWeeklyVal = {}
    VietnamWeeklyVal = {}
    TimorWeeklyVal = {}
    ThailandWeeklyVal = {}
    LaosWeeklyVal = {}
    IndonesiaWeeklyVal = {}
    for row in dailyhosp:
        currentDate = parser.parse((row['date']))
        year = int(currentDate.strftime("%Y"))
        month = int(currentDate.strftime("%m"))
        day = int(currentDate.strftime("%d"))
        isoDate = datetime.datetime(year, month, day).isocalendar()
        firstDay = datetime.date.fromisocalendar(isoDate.year, isoDate.week, 7)
        currentDate = datetime.date(year, month, day)
        if isinstance(row['new_cases'], float):
            if str(isoDate.week) + str(year) in WeeklyVal:
                SEAWeeklyVal[str(firstDay)] += row['new_cases']
            else:
                SEAWeeklyVal[str(firstDay)] = row['new_cases']
                WeeklyVal.append(str(isoDate.week) +
                                 str(year))
            if currentDate in ICUDates:
                SEAICUDict[str(currentDate)] += row['new_cases']
            else:
                ICUDates.append(currentDate)
                SEAICUDict[str(currentDate)] = row['new_cases']
            if row['location'] == "Singapore":
                SingaporeICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in SingaporeWeeklyVal:
                    SingaporeWeeklyVal[str(firstDay)] += row['new_cases']
                    print(SingaporeWeeklyVal)
                else:
                    SingaporeWeeklyVal[str(firstDay)] = row['new_cases']

            elif row['location'] == "Brunei":
                BruneiICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in BruneiWeeklyVal:
                    BruneiWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    BruneiWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Myanmar":
                MyanmarICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in MyanmarWeeklyVal:
                    MyanmarWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    MyanmarWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Malaysia":
                MalaysiaICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in MalaysiaWeeklyVal:
                    MalaysiaWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    MalaysiaWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Cambodia":
                CambodiaICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in CambodiaWeeklyVal:
                    CambodiaWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    CambodiaWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Philippines":
                PhillipinesICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in PhilippinesWeeklyVal:
                    PhilippinesWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    PhilippinesWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Vietnam":
                VietnamICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in VietnamWeeklyVal:
                    VietnamWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    VietnamWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Timor":
                TimorICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in TimorWeeklyVal:
                    TimorWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    TimorWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Thailand":
                ThailandICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in ThailandWeeklyVal:
                    ThailandWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    ThailandWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Laos":
                LaosICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in LaosWeeklyVal:
                    LaosWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    LaosWeeklyVal[str(firstDay)] = row['new_cases']
            elif row['location'] == "Indonesia":
                IndonesiaICUDict[str(currentDate)] = row['new_cases']
                if str(firstDay) in IndonesiaWeeklyVal:
                    IndonesiaWeeklyVal[str(firstDay)] += row['new_cases']
                else:
                    IndonesiaWeeklyVal[str(firstDay)] = row['new_cases']
        # else:
        #     if str(isoDate.week) + str(year) in WeeklyVal:
        #         SEAWeeklyVal[str(firstDay)] += 0
        #     else:
        #         SEAWeeklyVal[str(firstDay)] = 0
        #         WeeklyVal.append(str(isoDate.week) +
        #                          str(year))
        #     if currentDate in ICUDates:
        #         SEAICUDict[str(currentDate)] += 0
        #     else:
        #         ICUDates.append(currentDate)
        #         SEAICUDict[str(currentDate)] = 0
        #     if row['location'] == "Singapore":
        #         SingaporeICUDict[str(currentDate)] = 0
        #         if str(firstDay) in SingaporeWeeklyVal:
        #             SingaporeWeeklyVal[str(firstDay)] += 0
        #         else:
        #             SingaporeWeeklyVal[str(firstDay)] = 0
        #
        #     elif row['location'] == "Brunei":
        #         BruneiICUDict[str(currentDate)] = 0
        #         if str(firstDay) in BruneiWeeklyVal:
        #             BruneiWeeklyVal[str(firstDay)] += 0
        #         else:
        #             BruneiWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Myanmar":
        #         MyanmarICUDict[str(currentDate)] = 0
        #         if str(firstDay) in MyanmarWeeklyVal:
        #             MyanmarWeeklyVal[str(firstDay)] += 0
        #         else:
        #             MyanmarWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Malaysia":
        #         MalaysiaICUDict[str(currentDate)] = 0
        #         if str(firstDay) in MalaysiaWeeklyVal:
        #             MalaysiaWeeklyVal[str(firstDay)] += 0
        #         else:
        #             MalaysiaWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Cambodia":
        #         CambodiaICUDict[str(currentDate)] = 0
        #         if str(firstDay) in CambodiaWeeklyVal:
        #             CambodiaWeeklyVal[str(firstDay)] += 0
        #         else:
        #             CambodiaWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Philippines":
        #         PhillipinesICUDict[str(currentDate)] = 0
        #         if str(firstDay) in PhilippinesWeeklyVal:
        #             PhilippinesWeeklyVal[str(firstDay)] += 0
        #         else:
        #             PhilippinesWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Vietnam":
        #         VietnamICUDict[str(currentDate)] = 0
        #         if str(firstDay) in VietnamWeeklyVal:
        #             VietnamWeeklyVal[str(firstDay)] += 0
        #         else:
        #             VietnamWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Timor":
        #         TimorICUDict[str(currentDate)] = 0
        #         if str(firstDay) in TimorWeeklyVal:
        #             TimorWeeklyVal[str(firstDay)] += 0
        #         else:
        #             TimorWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Thailand":
        #         ThailandICUDict[str(currentDate)] = 0
        #         if str(firstDay) in ThailandWeeklyVal:
        #             ThailandWeeklyVal[str(firstDay)] += 0
        #         else:
        #             ThailandWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Laos":
        #         LaosICUDict[str(currentDate)] = 0
        #         if str(firstDay) in LaosWeeklyVal:
        #             LaosWeeklyVal[str(firstDay)] += 0
        #         else:
        #             LaosWeeklyVal[str(firstDay)] = 0
        #     elif row['location'] == "Indonesia":
        #         IndonesiaICUDict[str(currentDate)] = 0
        #         if str(firstDay) in IndonesiaWeeklyVal:
        #             IndonesiaWeeklyVal[str(firstDay)] += 0
        #         else:
        #             IndonesiaWeeklyVal[str(firstDay)] = 0
    return render_template("fifthpage.html",
                           SingaporeICUDict=SingaporeICUDict,
                           BruneiICUDict=BruneiICUDict, MyanmarICUDict=MyanmarICUDict,
                           MalaysiaICUDict=MalaysiaICUDict,
                           CambodiaICUDict=CambodiaICUDict, PhillipinesICUDict=PhillipinesICUDict,
                           VietnamICUDict=VietnamICUDict, TimorICUDict=TimorICUDict,
                           ThailandICUDict=ThailandICUDict, LaosICUDict=LaosICUDict,
                           IndonesiaICUDict=IndonesiaICUDict, SEAICUDict=SEAICUDict,
                           SEAWeeklyVal=SEAWeeklyVal, SingaporeWeeklyVal=SingaporeWeeklyVal,
                           BruneiWeeklyVal=BruneiWeeklyVal, MyanmarWeeklyVal=MyanmarWeeklyVal,
                           MalaysiaWeeklyVal=MalaysiaWeeklyVal,
                           CambodiaWeeklyVal=CambodiaWeeklyVal, PhilippinesWeeklyVal=PhilippinesWeeklyVal,
                           VietnamWeeklyVal=VietnamWeeklyVal, TimorWeeklyVal=TimorWeeklyVal,
                           ThailandWeeklyVal=ThailandWeeklyVal, LaosWeeklyVal=LaosWeeklyVal,
                           IndonesiaWeeklyVal=IndonesiaWeeklyVal
                           )

# displays fourth page
@app.route("/fourthpage")
def fourthpage():
    # query 4
    dailycases = mycol1.find({}, {"_id": 0, "location": 1, "new_cases": 1, "date": 1})
    # query 6
    dailydeaths = mycol1.find({}, {"_id": 0, "location": 1, "new_deaths": 1, "date": 1})
    # Covid-19 Cases for each SEA country to date
    Coviddates = list()
    SingaporeDict = {}
    BruneiDict = {}
    MyanmarDict = {}
    MalaysiaDict = {}
    CambodiaDict = {}
    PhillipinesDict = {}
    VietnamDict = {}
    TimorDict = {}
    ThailandDict = {}
    LaosDict = {}
    IndonesiaDict = {}
    SEADict = {}
    deathDates = list()
    SingaporeDeaths = {}
    BruneiDeaths = {}
    MyanmarDeaths = {}
    MalaysiaDeaths = {}
    CambodiaDeaths = {}
    PhillipinesDeaths = {}
    VietnamDeaths = {}
    TimorDeaths = {}
    ThailandDeaths = {}
    LaosDeaths = {}
    IndonesiaDeaths = {}
    SEADeaths = {}
    for row in dailycases:
        currentDate = parser.parse((row['date']))
        year = int(currentDate.strftime("%Y"))
        month = int(currentDate.strftime("%m"))
        day = int(currentDate.strftime("%d"))
        currentDate = datetime.date(year, month, day)
        if isinstance(row['new_cases'], float):
            if currentDate in Coviddates:
                SEADict[str(currentDate)] += int(row['new_cases'])
            else:
                Coviddates.append(currentDate)
                SEADict[str(currentDate)] = int(row['new_cases'])
            if row['location'] == "Singapore":
                SingaporeDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Brunei":
                BruneiDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Myanmar":
                MyanmarDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Malaysia":
                MalaysiaDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Cambodia":
                CambodiaDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Philippines":
                PhillipinesDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Vietnam":
                VietnamDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Timor":
                TimorDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Thailand":
                ThailandDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Laos":
                LaosDict[str(currentDate)] = row['new_cases']
            elif row['location'] == "Indonesia":
                IndonesiaDict[str(currentDate)] = row['new_cases']
        else:
            if currentDate in Coviddates:
                SEADict[str(currentDate)] += 0
            else:
                Coviddates.append(currentDate)
                SEADict[str(currentDate)] = 0
            if row['location'] == "Singapore":
                SingaporeDict[str(currentDate)] = 0
            elif row['location'] == "Brunei":
                BruneiDict[str(currentDate)] = 0
            elif row['location'] == "Myanmar":
                MyanmarDict[str(currentDate)] = 0
            elif row['location'] == "Malaysia":
                MalaysiaDict[str(currentDate)] = 0
            elif row['location'] == "Cambodia":
                CambodiaDict[str(currentDate)] = 0
            elif row['location'] == "Philippines":
                PhillipinesDict[str(currentDate)] = 0
            elif row['location'] == "Vietnam":
                VietnamDict[str(currentDate)] = 0
            elif row['location'] == "Timor":
                TimorDict[str(currentDate)] = 0
            elif row['location'] == "Thailand":
                ThailandDict[str(currentDate)] = 0
            elif row['location'] == "Laos":
                LaosDict[str(currentDate)] = 0
            elif row['location'] == "Indonesia":
                IndonesiaDict[str(currentDate)] = 0

    for row in dailydeaths:
        currentDate = parser.parse((row['date']))
        year = int(currentDate.strftime("%Y"))
        month = int(currentDate.strftime("%m"))
        day = int(currentDate.strftime("%d"))
        currentDate = datetime.date(year, month, day)
        if isinstance(row['new_deaths'], float):
            print(currentDate)
            if currentDate in deathDates:
                SEADeaths[str(currentDate)] += row['new_deaths']
            else:
                deathDates.append(str(currentDate))
                SEADeaths[str(currentDate)] = row['new_deaths']
            if row['location'] == "Singapore":
                SingaporeDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Brunei":
                BruneiDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Myanmar":
                MyanmarDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Malaysia":
                MalaysiaDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Cambodia":
                CambodiaDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Philippines":
                PhillipinesDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Vietnam":
                VietnamDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Timor":
                TimorDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Thailand":
                ThailandDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Laos":
                LaosDeaths[str(currentDate)] = row['new_deaths']
            elif row['location'] == "Indonesia":
                IndonesiaDeaths[str(currentDate)] = row['new_deaths']
        else:
            if currentDate in deathDates:
                SEADeaths[str(currentDate)] += 0
            else:
                deathDates.append(str(currentDate))
                SEADeaths[str(currentDate)] = 0
            if row['location'] == "Singapore":
                SingaporeDeaths[str(currentDate)] = 0
            elif row['location'] == "Brunei":
                BruneiDeaths[str(currentDate)] = 0
            elif row['location'] == "Myanmar":
                MyanmarDeaths[str(currentDate)] = 0
            elif row['location'] == "Malaysia":
                MalaysiaDeaths[str(currentDate)] = 0
            elif row['location'] == "Cambodia":
                CambodiaDeaths[str(currentDate)] = 0
            elif row['location'] == "Philippines":
                PhillipinesDeaths[str(currentDate)] = 0
            elif row['location'] == "Vietnam":
                VietnamDeaths[str(currentDate)] = 0
            elif row['location'] == "Timor":
                TimorDeaths[str(currentDate)] = 0
            elif row['location'] == "Thailand":
                ThailandDeaths[str(currentDate)] = 0
            elif row['location'] == "Laos":
                LaosDeaths[str(currentDate)] = 0
            elif row['location'] == "Indonesia":
                IndonesiaDeaths[str(currentDate)] = 0

    return render_template("fourthpage.html", SingaporeDict=SingaporeDict,
                           BruneiDict=BruneiDict, MyanmarDict=MyanmarDict, MalaysiaDict=MalaysiaDict,
                           CambodiaDict=CambodiaDict, PhillipinesDict=PhillipinesDict, VietnamDict=VietnamDict,
                           TimorDict=TimorDict, ThailandDict=ThailandDict, LaosDict=LaosDict,
                           IndonesiaDict=IndonesiaDict, SEADict=SEADict,
                           SingaporeDeaths=SingaporeDeaths,
                           BruneiDeaths=BruneiDeaths, MyanmarDeaths=MyanmarDeaths, MalaysiaDeaths=MalaysiaDeaths,
                           CambodiaDeaths=CambodiaDeaths, PhillipinesDeaths=PhillipinesDeaths,
                           VietnamDeaths=VietnamDeaths, TimorDeaths=TimorDeaths,
                           ThailandDeaths=ThailandDeaths, LaosDeaths=LaosDeaths,
                           IndonesiaDeaths=IndonesiaDeaths, SEADeaths=SEADeaths
                           )


# mongo db
@app.route('/')
def showData():
    # 3rd , declare a variable to store the queries you want to find
    # 11 query
    vaccinatedtotal = {}
    vaccinatedtotal = personfullyvaccinated

    # 2nd query
    # totalcases = list()

    totalcaseslist = []
    totalcasesnumber = []
    # make the dictionary to list so can display in chartjs
    for i in totalnumberofcasestodate:
        totalcaseslist.append(i['_id'])

        totalcasesnumber.append(i['Total_cases'])

    # 10 query
    countrypeoplevaccinated = []
    countryname = []
    for x in totalvaccineSEA:
        countryname.append(x['COUNTRY'])
        countrypeoplevaccinated.append(x['PERSONS_FULLY_VACCINATED'])
    # 1st query
    totalconfirmedcase = {}
    totalconfirmedcase = totalcase

    # return render template to index html. and store the variable in the variable so in the html you can call the variable to display it.
    return render_template('index.html', vaccinatedtotal=vaccinatedtotal, totalcaseslist=totalcaseslist,
                           totalcasesnumber=totalcasesnumber,
                           countrypeoplevaccinated=countrypeoplevaccinated, countryname=countryname,
                           totalconfirmedcase=totalconfirmedcase
                           )


@app.route('/secondpage')
def secondpage():
    # 10 query
    totaldeath = []
    totalcases = []
    location = []
    for x in percentagetotaldeath:
        totaldeath.append(x['Total Deaths'])
        totalcases.append(x['Total_Cases'])
        location.append(x['_id'])

    # 9 query
    totaldeathwithinpop = []
    totalcaseswithinpop = []
    population = []
    countryname = []
    for y in casesanddeathwithinpopulation:
        totalcaseswithinpop.append(y['Total Cases'])
        totaldeathwithinpop.append(y['Total Deaths'])
        population.append(y['Population'])
        countryname.append(y['_id'])

    return render_template(
        "secondpage.html", totalcases=totalcases, totaldeath=totaldeath, location=location,
        totalcaseswithinpop=totalcaseswithinpop, totaldeathwithinpop=totaldeathwithinpop, population=population,
        countryname=countryname

    )


if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
