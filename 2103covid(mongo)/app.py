

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

#query 7 aggregate always use this format
personfullyvaccinated = mycol.aggregate( [{
    "$group" : 
        {"_id" : "", 
         "SUM": {"$sum" : '$PERSONS_FULLY_VACCINATED'}
         }}
    ])


#mongo db 
@app.route('/')
def showData():
        #3rd , declare a variable to store the queries you want to find 
        vaccinatedtotal={}
        vaccinatedtotal= personfullyvaccinated 
        
        #return render template to index html. and store the variable in the variable so in the html you can call the variable to display it. 
        return render_template('index.html', vaccinatedtotal = vaccinatedtotal)
       
  

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
