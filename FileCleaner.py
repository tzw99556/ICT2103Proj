#!/usr/bin/env python3
import os 
import pandas as pd
import json 
import csv

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
        self.dest_file_name = f"[JSON]-{os.path.splitext(source_file_name)[0]}.csv"
        
    def csv_to_json(self):
        jsonArray = []   
        #read csv file
        with open(self.source_file_name, encoding='utf-8') as csv_f: 
            #load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csv_f) 

            #convert each csv row into python dict
            for row in csvReader: 
                #add this python dict to json array
                jsonArray.append(row)
    
        #convert python jsonArray to JSON String and write to file
        with open(self.dest_file_name, 'w', encoding='utf-8') as json_f: 
            jsonString = json.dumps(jsonArray, indent=4)
            json_f.write(jsonString)
        
def main():
    countries_to_keep = ["Brunei", "Myanmar", "Cambodia", "Timor", "Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand", "Vietnam", "Laos"]
    columns_to_keep= ["iso_code", "location", "date", "total_cases", "new_cases", "total_deaths", "new_deaths", "total_cases_per_million", "new_cases_per_million", "total_deaths_per_million", "new_deaths_per_million", "icu_patients", "icu_patients_per_million", "hosp_patients", "hosp_patients_per_million", "weekly_icu_admissions", "weekly_icu_admissions_per_million", "weekly_hosp_admissions", "weekly_hosp_admissions_per_million", "total_tests", "new_tests", "total_tests_per_thousand", "new_tests_per_thousand", "positive_rate", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters" , "new_vaccinations", "total_vaccinations_per_hundred", "people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred", "total_boosters_per_hundred", "stringency_index", "population", "population_density"]
    worldindata = FileCleaner("worldindata-covid-allcountries.csv")
    worldindata.clean_raw_data(countries_to_keep, columns_to_keep)
    json_manager = JsonManager(worldindata.dest_file_name)
    json_manager.csv_to_json()

if __name__ == "__main__":
    main()




