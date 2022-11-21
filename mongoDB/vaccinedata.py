import pymongo
import json

#replace this link with your own mongodb connection. 
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["CovidSEA"]
mycol = mydb["worldindata"]
mycol2 = mydb["vaccination"]

with open('[JSON]-[cleaned]-worldindata-covid.csv') as file1:

        file_data1 = json.load(file1)
    
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else insert_one is used
#insert all json data inside collectiin
if isinstance(file_data1, list):
    mycol.insert_many(file_data1) 

# Loading or Opening the json file
with open('[JSON]-[cleaned]-vaccination-data.csv') as file:
   
    file_data = json.load(file)
    
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else insert_one is used
#insert all json data inside collectiin
if isinstance(file_data, list):
    mycol2.insert_many(file_data) 
