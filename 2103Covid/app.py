import sys

import cur as cur
from flask import Flask,render_template
from flask import request,jsonify
from pymongo import MongoClient
import mysql.connector
import mariaDB
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mariadb
app = Flask(__name__)

#mongodb
client = MongoClient("mongodb://127.0.0.1:27017")
mydb = client['CovidSEA']
mycol = mydb['Covid19SEAdata']
app = Flask('2103proj')
 
# conn = mariadb.connect(
#          host='localhost',
#          user='root',
#          password='Martinwee1',
#          database='covid_proj_sea')
# cur = conn.cursor()

#mariadb
@app.route("/maria")
def showSeaData():
    # Connecting to mysql database

 
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="Martinwee1",
                                database="covid_sea_proj")
    mycursor = mydb.cursor()


    # # Fetching Data From mysql to my python progame
    mycursor.execute("select t.total_cases,date from cases_and_death t, date d where d.date_id = t.date_id and date = '19/9/2022';")
    result = mycursor.fetchall()
    print(result)

   #declare the labels you want to display in the graph
    labels = list()
    #for each row in the sql statement append it into label's list. 
    for row in result:
      labels.append(row)

    #declare the values you want to display in the graph 
    values = list()
    i = 0

    #for each row in sql statement , append it to value's list
    for row in result:
       values.append(row[i])
    print(values)
    # return view of mariahtml , store values in to value variable and labels into labels variable so we can use it to call the 
    # variables in the html page using {{values}}
    return render_template('maria.html', values=values, labels=labels)





    # Names = []
    # Marks = []
    
    # for i in mycursor:
    #     Names.append(i[0])
    #     Marks.append(i[1])
        
    # print("Name of Students = ", Names)
    # print("Marks of Students = ", Marks)
    
    
    # # Visulizing Data using Matplotlib
    # plt.bar(Names, Marks)
    # plt.ylim(0, 5)
    # plt.xlabel("Name of Students")
    # plt.ylabel("Marks of Students")
    # plt.title("Student's Information")
    # showplot = plt.show()
    # return render_template("maria.html") 



@app.route("/")
def home():
   return render_template("")
    

#mongo db 
@app.route('/showData')
def showData():
    showDataList = []
    for i in mycol.find({},{"total_deaths":19265.0}):
        showDataList.append(i)
  
    return jsonify(showDataList)


# mongo db
# @app.route('/showData', methods=['GET'])
# def index():
    # cur.execute("select t.total_cases from cases_and_death t, date d where d.date_id = t.date_id and date = '19/9/2022'")
    # data = cur.fetchall()
    # # return render_template('maria.html', values=data)

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)




