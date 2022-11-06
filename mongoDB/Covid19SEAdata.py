import pymongo
import json

#replace this link with your own mongodb connection. 
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["CovidSEA"]
mycol = mydb["Covid19SEAdata"]

# Loading or Opening the json file
with open('[JSON]-[cleaned]-worldindata-covid-allcountries.csv') as file:
    file_data = json.load(file)
     
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else insert_one is used
#insert all json data inside collectiin
if isinstance(file_data, list):
    mycol.insert_many(file_data) 
else:
    mycol.insert_one(file_data)

#for each data in collections , print out the values. 
for x in mycol.find():
  print(x)
 