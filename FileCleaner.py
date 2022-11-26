import os 
import pandas as pd
import json 
import csv
from datetime import datetime 

class FileCleaner:
    """Used to obtain a .csv file that contains only countries and columns of interest"""
    def __init__(self, source_file_name:str):
        self.source_file_name = source_file_name
        self.dest_file_name = f"[cleaned]-{os.path.splitext(source_file_name)[0]}.csv"
    
    def clean_raw_data(self, countries:list, columns: list):
        """ Returns a csv file containing data for specified countries. Will contain only columns specified in columns list"""
        with open(self.source_file_name, 'r') as file, open(self.dest_file_name, 'w') as new_file:
            lines = file.readlines()
            new_file.write(lines[0]) # writes headers
            for line in lines:
                for country in countries:
                    if country in line:
                        new_file.write(line)
        self.keep_columns(columns)
    
    def keep_columns(self, columns:list):
        data = pd.read_csv(self.dest_file_name, index_col=False)
        data[columns].to_csv(self.dest_file_name, index=False)
        print(f"{self.dest_file_name} created")

class JsonManager:
    "Used to generate json file for mongoDB"
    def __init__(self, source_file_name):
        self.source_file_name = source_file_name
        self.dest_file_name = f"[JSON]-{os.path.splitext(self.source_file_name)[0]}.csv"
    
    def change_file(self, source_file_name):
        self.source_file_name = source_file_name
        self.dest_file_name = f"[JSON]-{os.path.splitext(source_file_name)[0]}.csv"

    def csv_to_json(self):
        jsonArray = []   
        #read csv file
        with open(self.source_file_name, encoding='utf-8') as csv_f: 
            #load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csv_f) 
            #convert each csv row into python dict
            for row in csvReader: 
                # converts values to floats if applicable
                for key, value in row.items():
                    try:
                        temp = float(value)
                        row[key] = temp
                    except ValueError:
                        continue
                jsonArray.append(row)
    
        #convert python jsonArray to JSON String and write to file
        with open(self.dest_file_name, 'w', encoding='utf-8') as json_f: 
            jsonString = json.dumps(jsonArray, indent=4)
            json_f.write(jsonString)
        
def main():
    # Cleans - worldindata-covid-allcountries.csv 
    worldindata_cleaner = FileCleaner("worldindata-covid.csv")
    countries_to_keep = ["Brunei", "Myanmar", "Cambodia", "Timor", "Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand", "Vietnam", "Laos"]
    columns_to_keep= ["iso_code", "location", "date", "total_cases", "new_cases", "total_deaths", "new_deaths", "hosp_patients", "weekly_hosp_admissions", "stringency_index", "population", "population_density"]
    worldindata_cleaner.clean_raw_data(countries_to_keep, columns_to_keep)
    json_manager = JsonManager(worldindata_cleaner.dest_file_name)
    json_manager.csv_to_json()

    # Cleans - vaccination-data.csv
    vaccinationdata_cleaner = FileCleaner("vaccination-data.csv")
    countries_to_keep = ["Brunei", "Myanmar", "Cambodia", "Timor", "Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand", "Viet Nam", "Lao People's Democratic Republic"]
    columns_to_keep = ["COUNTRY","ISO3","TOTAL_VACCINATIONS","PERSONS_FULLY_VACCINATED", "VACCINES_USED"]
    vaccinationdata_cleaner.clean_raw_data(countries_to_keep, columns_to_keep)
    json_manager = JsonManager(vaccinationdata_cleaner.dest_file_name)
    json_manager.csv_to_json()

if __name__ == "__main__":
    main()




