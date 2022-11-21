import sys
from flask import Flask,render_template, url_for
from flask import request,jsonify
import mysql.connector
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pymongo



app = Flask(__name__)

#mongodb
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")   
#db
mydb = client['CovidSEA']
#collections
mycol = mydb['Covid19SEAdata']


app = Flask('2103proj')




#1st , any mongodb query will be declared through this statement '
#this query is finding an iso_code where is labelled as "BRN"
myquery = { "iso_code": "BRN"}

#2nd store the query using mycol which links to your collection and store in variable mydoc.
#for this , you if its . find means find everything in collection you can replace it with 
#insertmany , insert one depending on the mongo query you need. 
mydoc = mycol.find(myquery)



#mongo db 
@app.route('/')
def showData():

        #3rd , declare a variable to store the queries you want to find 
        h = mydoc 
            
        #return render template to index html. and store the variable in the variable so in the html you can call the variable to display it. 
        return render_template('index.html', h=h)
       
  



if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
