

import sys
from flask import Flask,render_template, url_for
from flask import request,jsonify
import mysql.connector
import pymongo



app = Flask(__name__)

#mongodb
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")   
#db
mydb = client['CovidSEA']
#collections
mycol = mydb['vaccination']
mycol1 = mydb['worldindata']
app = Flask('2103proj')


#1st , any mongodb query will be declared through this statement '
#this query is finding an iso_code where is labelled as "BRN"
#myquery = { "group": "BRN"}



#2nd store the query using mycol which links to your collection and store in variable mydoc.
#for this , you if its . find means find everything in collection you can replace it with 
#insertmany , insert one depending on the mongo query you need. 

#query 11 aggregate always use this format
personfullyvaccinated = mycol.aggregate( [{
    "$group" : 
        {"_id" : "", 
         "SUM": {"$sum" : '$PERSONS_FULLY_VACCINATED'}
         }}
    ])

# query 2
totalnumberofcasestodate = mycol1.aggregate(
        [{ "$group": 
        {"_id": '$location',
        "Total_cases":{"$max":'$total_cases'},"data":{"$last": '$date'}

        } 
        
        
        }])

#query 10
totalvaccineSEA = mycol.find({},  {"_id": 0, "COUNTRY": 1,"PERSONS_FULLY_VACCINATED": 1})

#query 8
percentagetotaldeath = mycol1.aggregate(
         [{ "$group": 
        {"_id": '$location',
        "Total_Cases":{"$last":'$total_cases'},
        "Total Deaths":{"$last": "$total_deaths"},
        "Latest Date": {"$last": "$date"}

        } 
        
        
        }])


#query 9
casesanddeathwithinpopulation = mycol1.aggregate([{ "$group": 
        {"_id": '$location',
        "Total Cases":{"$last":'$total_cases'},
        "Total Deaths":{"$last": "$total_deaths"},
        "Population": {"$max": "$population"},
        "Date":{"$last": "$date"}

        } 
        
        
        }])

#query 6
totalcase = mycol1.aggregate(
    [{
        "$group":{"_id": "$location", "total": {"$last": "$total_cases"}}},{"$group":{"_id": "null", "TotalCase": {"$sum": "$total"}}}])






#mongo db 
@app.route('/')
def showData():
        #3rd , declare a variable to store the queries you want to find 
        #11 query
        vaccinatedtotal={}
        vaccinatedtotal= personfullyvaccinated 

        #2nd query
       # totalcases = list()
        
        totalcaseslist = []
        totalcasesnumber = []
        # make the dictionary to list so can display in chartjs
        for i in totalnumberofcasestodate:
                totalcaseslist.append(i['_id'])
       
                totalcasesnumber.append(i['Total_cases'])

        #10 query 
        countrypeoplevaccinated =[]
        countryname =[]
        for x in totalvaccineSEA:
                countryname.append(x['COUNTRY'])
                countrypeoplevaccinated.append(x['PERSONS_FULLY_VACCINATED'])
        #1st query 
        totalconfirmedcase={}
        totalconfirmedcase=  totalcase

        
        #return render template to index html. and store the variable in the variable so in the html you can call the variable to display it. 
        return render_template('index.html', vaccinatedtotal = vaccinatedtotal, totalcaseslist =totalcaseslist, totalcasesnumber=totalcasesnumber,
        countrypeoplevaccinated = countrypeoplevaccinated , countryname = countryname, totalconfirmedcase = totalconfirmedcase
        )
       
@app.route('/secondpage')
def secondpage():
          #10 query 
        totaldeath =[]
        totalcases =[]
        location = []
        for x in percentagetotaldeath:
                totaldeath.append(x['Total Deaths'])
                totalcases.append(x['Total_Cases'])
                location.append(x['_id'])


        #9 query 
        totaldeathwithinpop = []
        totalcaseswithinpop = []
        population =[]
        countryname = []
        for y in casesanddeathwithinpopulation:
                totalcaseswithinpop.append(y['Total Cases'])
                totaldeathwithinpop.append(y['Total Deaths'])
                population.append(y['Population'])
                countryname.append(y['_id'])


        return render_template(
                "secondpage.html", totalcases=totalcases, totaldeath=totaldeath, location=location,
        totalcaseswithinpop=totalcaseswithinpop , totaldeathwithinpop =totaldeathwithinpop , population = population, 
        countryname = countryname
        
        )

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
