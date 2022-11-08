#!/usr/bin/env python3
import mariadb
import sys
import pandas as pd
import datetime

# Connect to MariaDB Platform 
class MariaDB_Manager:
    """
    User credentials provided must have authorization to mariadb additionally, database must already exist
    create database in mariadb, add user and corresponding authorization. 
    """
    def __init__(self, user:str, password:str, host:str, port:int, database:str):
        self.user = user
        self.password = password
        self.host = host # typically localhost unless hosted on cloud
        self.port = port # by default port 3306, use /status in mariadb cli to verify port id. 
        self.database = database # must already exists in maraidb client

        self.errorlog = []
        self.errorlog_txt = f"{self.database}-errorlog-{datetime.datetime.now()}.txt"
        self.allQueries = []

        try:
            self.conn = mariadb.connect(
                user= self.user,
                password= self.password,
                host= self.host,
                port= self.port,
                database= self.database,
                autocommit=True
                )
            self.cur = self.conn.cursor()
    
        except mariadb.Error as e:
            with open(self.errorlog_txt, 'a') as f:
                f.write(f"Error connecting to MariaDB Platform: {e}\n")
                f.write(f"mariaDb credentials provided: {self.user}\n{self.password}\n{self.host}\n{self.port}\n{self.database}\n")
            print(f"Error connecting to MariaDB Platform: {e}\n")
            sys.exit(1)
    
    def single_query_executor(self, query):
        """Helper function that executes mariadb queries, note .commit() must be included if
        autocommit=False in connection initializer. Returns self.cur object an iterable that stores results of queries.
        """
        try: 
            self.cur.execute(query)          
        except mariadb.Error as e: 
            with open(self.errorlog_txt, 'a') as f:
                f.write(f"Error: {e}\n")
            print(f"Error: {e}\n")
            return None
        self.allQueries.append(query)
        return self.cur

    def batch_query_executor(self, list_of_queries: list): 
        """Executes multiple queries sequentially follow order provided in list_of_queries"""
        for query in list_of_queries:
            self.single_query_executor(query)
        return 
    
    def insert_executor(self, table_name:str, column_names:list, tuple_list:list):
        """Formats query for standard insertion and invokes .single_query_executor() to perform insertion operation
        """
        for tup in tuple_list:
            if (len(tup) > 1):
                column_str = ", ".join(column_names)
                query = f"INSERT INTO {table_name} ({column_str}) VALUES {tup};" 
            else:
                column_str = "".join(column_names)
                values = "".join(tup)
                query = f"INSERT INTO {table_name} ({column_str}) VALUES ('{values}');" 
            self.single_query_executor(query)

    def get_id_mapppings(self, query) -> dict:
        """Obtain dictionary of [variable]:[variable_id] e.g.,., maps each date / country to its corresponding date_id / country_id"""
        self.single_query_executor(query)
        id_mappings = {}
        for variable, variable_id in self.cur:
            id_mappings[variable] = variable_id
        return id_mappings
    
    def map_dates(self) -> dict:
        """Obtain date-date_id mappings"""
        query = f"SELECT date, date_id FROM Date;"
        date_dictionary = self.get_id_mapppings(query)
        return date_dictionary

    def map_countries(self) -> dict:
        """Obtain country_iso-country_id mappings"""
        query = f"SELECT country_iso, country_id FROM Country;"
        countries_dictionary = self.get_id_mapppings(query)
        return countries_dictionary
    
    def generate_sql_file(self, file_name: str): 
        with open(file_name, "w") as file:
            file.write(f"CREATE DATABASE IF NOT EXISTS covid_sea_proj;\n")
            file.write(f"USE covid_sea_proj;\n")
            for query in self.allQueries:
                file.write(query)
                file.write('\n')                
        print(f"{file_name} containing SQL commands generated. \n mariadb > source [path_to_file]")
    
    def drop_all_tables(self):
        """For debugging, quick method to drop all tables from database"""
        tables = ["Hospital_admission", "Cases_and_death", "Country_information", "Vaccination", "Date", "Country"]
        for table in tables:
            query = f"DROP TABLE {table}"
            self.single_query_executor(query)
        print(f"Dropped {tables}, exiting")
        sys.exit(1)

class Tuple_Generator:
    """Class helps to generate and format dataframes"""
    def __init__(self, source_file_name: str):
        self.source_file_name = source_file_name
        self.df = pd.read_csv(self.source_file_name, index_col=False)
        
    def get_columns(self, columns_of_interest: list) -> pd.DataFrame:
        df = self.df[columns_of_interest]
        df = df.fillna(0) # Converts NaN values to 0 (Find a better number)
        return df[columns_of_interest]
        
    def get_List_Of_Tuples(self, a_df) -> list:
        return list(a_df.itertuples(index=False, name=None))

    def add_date_id_column(self, date_dict):
        """Adds a date ID Column to dataframe"""
        date_df = self.df["date"]
        self.df["date_id"] = [date_dict[date] if date in date_dict.keys() else " " for date in date_df] 

    def add_map_id_column(self, map_dict, label):
       """Adds a country_id Column to dataframe"""
       iso_code_df = self.df[label]
       self.df["country_id"] = [map_dict[iso] if iso in map_dict.keys() else " " for iso in iso_code_df] 

class TableBuilder_Worldindata:
    """Modify functions below to alter mariadb tables"""
    def __init__(self, mariadb_connector) -> None:
        self.mariadb_connector = mariadb_connector

    def create_tables(self):
        """Creates Country, Date, Country_information, Cases_and_death, Hospital_admission tables"""
        worldindata_create_table_queries = [
        "CREATE TABLE IF NOT EXISTS Country (country_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT, country_name VARCHAR(30) UNIQUE NOT NULL, country_iso VARCHAR(3) UNIQUE NOT NULL, PRIMARY KEY (country_id));",
        "CREATE TABLE IF NOT EXISTS Date (date_id INT UNSIGNED NOT NULL AUTO_INCREMENT, date VARCHAR(10), PRIMARY KEY (date_id));",
        "CREATE TABLE IF NOT EXISTS Country_information (population_density DECIMAL(6,2), population INT UNSIGNED, stringency_index TINYINT UNSIGNED NOT NULL, date_id INT UNSIGNED NOT NULL, country_id TINYINT UNSIGNED, PRIMARY KEY(date_id, country_id), FOREIGN KEY (date_id) REFERENCES Date(date_id), FOREIGN KEY (country_id) REFERENCES Country(country_id));",
        "CREATE TABLE IF NOT EXISTS Cases_and_death (new_deaths INT UNSIGNED, total_deaths INT UNSIGNED, total_cases INT UNSIGNED, new_cases INT UNSIGNED, date_id INT UNSIGNED NOT NULL, country_id TINYINT UNSIGNED, PRIMARY KEY(date_id, country_id), FOREIGN KEY (date_id) REFERENCES Date(date_id), FOREIGN KEY (country_id) REFERENCES Country(country_id));",
        "CREATE TABLE IF NOT EXISTS Hospital_admission (hosp_patients INT UNSIGNED, weekly_hosp_admissions INT UNSIGNED, date_id INT UNSIGNED NOT NULL, country_id TINYINT UNSIGNED, PRIMARY KEY(date_id, country_id), FOREIGN KEY (date_id) REFERENCES Date(date_id), FOREIGN KEY (country_id) REFERENCES Country(country_id));",
        ]
        self.mariadb_connector.batch_query_executor(worldindata_create_table_queries)

    def populate_a_new_table(self, worldindata_tuples):
        # (1) get df for table using worldindata_tuples.get_columns(["column_you_want"]) 
        # (2) convert df into a list of tuples using get_List_Of_Tuples("df")
        # (3) pass database tables columns to insert into 
        # (4) mariadb_conector.insert_executor("table_name", "columns_to_insert_into", "list_of_tuples")
        pass

    def populate_date_table(self, worldindata_tuples):
        # Populate Date table
        print("Populating date table: ")
        Date_df = worldindata_tuples.get_columns(["date"])  
        Date_tuples = worldindata_tuples.get_List_Of_Tuples(Date_df)
        Date_columns = ["date"]
        self.mariadb_connector.insert_executor("Date", Date_columns, Date_tuples)
        print("Date table created")
    
    def populate_country_table(self, worldindata_tuples):
        # Populate Country table
        print("Populating country table: ")
        Country_df = worldindata_tuples.get_columns(["location", "iso_code"]) 
        Country_tuples = set(worldindata_tuples.get_List_Of_Tuples(Country_df)) # country should be treated as set, dont need duplicated country and country codes
        Country_columns = ["country_name", "country_iso"]
        self.mariadb_connector.insert_executor("Country", Country_columns, Country_tuples)
        print("Country table created")

    def populate_country_information_table(self, worldindata_tuples):
        # Populate Country_information table
        print("Populating Country_information table: ")
        Country_information_df = worldindata_tuples.get_columns(["population_density", "population", "stringency_index", "date_id", "country_id"])
        Country_information_tuples = worldindata_tuples.get_List_Of_Tuples(Country_information_df)
        Country_information_columns = ["population_density", "population", "stringency_index", "date_id", "country_id"]
        self.mariadb_connector.insert_executor("Country_information", Country_information_columns, Country_information_tuples)
        print("Country_information table created")

    def populate_cases_and_death_table(self, worldindata_tuples):
        # Populate Cases_and_death table
        print("Populating Cases_and_death table: ")
        Cases_and_death_df = worldindata_tuples.get_columns(["new_deaths", "total_deaths","total_cases", "new_cases", "date_id", "country_id"])
        Cases_and_death_tuples = worldindata_tuples.get_List_Of_Tuples(Cases_and_death_df)
        Cases_and_death_columns = ["new_deaths", "total_deaths", "total_cases", "new_cases", "date_id", "country_id"]
        self.mariadb_connector.insert_executor("Cases_and_death", Cases_and_death_columns, Cases_and_death_tuples)
        print("Cases_and_death table created")

    def populate_hospital_admission_table(self, worldindata_tuples):
        # Populate Hospital_admission table
        print("Populating Hospital_admission table: ")
        Hospital_admission_df = worldindata_tuples.get_columns(["hosp_patients", "weekly_hosp_admissions", "date_id", "country_id"])
        Hospital_admission_tuples = worldindata_tuples.get_List_Of_Tuples(Hospital_admission_df)
        Hospital_admission_columns = ["hosp_patients", "weekly_hosp_admissions", "date_id", "country_id"]
        self.mariadb_connector.insert_executor("Hospital_admission", Hospital_admission_columns, Hospital_admission_tuples)
        print("Hospital_admission table created")
    
class TableBuilder_Vaccination:
    def __init__(self, mariadb_connector) -> None:
        self.mariadb_connector = mariadb_connector

    def create_tables(self):
        """Creates Country, Date, Country_information, Cases_and_death, Hospital_admission tables"""
        worldindata_create_table_queries = [
            "CREATE TABLE IF NOT EXISTS Vaccination (total_vaccinations INT UNSIGNED, persons_fully_vaccinated INT UNSIGNED, vaccines_used VARCHAR(400), country_id TINYINT UNSIGNED, PRIMARY KEY(country_id), FOREIGN KEY (country_id) REFERENCES Country(country_id));"
        ]
        self.mariadb_connector.batch_query_executor(worldindata_create_table_queries)

    def populate_Vaccination_table(self, vaccination_tuples):
        # Populate Date table
        print("Populating date table: ")
        Vaccination_df = vaccination_tuples.get_columns(["TOTAL_VACCINATIONS", "PERSONS_FULLY_VACCINATED", "VACCINES_USED", "country_id"])  
        Vaccination_tuples = vaccination_tuples.get_List_Of_Tuples(Vaccination_df)
        Vaccination_columns = ["total_vaccinations", "persons_fully_vaccinated", "vaccines_used", "country_id"]
        self.mariadb_connector.insert_executor("Vaccination", Vaccination_columns, Vaccination_tuples)
        print("Vaccination table created")

def main(): 
    """
    Workflow to create and populateworldindata tables in mariadb
        (1) Connect to mariadb client - pip3 install mariadb (and other related dependencies)
        (2) Create tables
        (3) Populate data and country tables, this will return auto-generated country_id and date_id
        (4) Insert country_id and date_id into dataframe.
        (5) Populate the remaining tables
        (6) Also generates a .sql script that can be executed in sql client to create database without having to connect to mariadb client in python
         
    **** Alternatively, run the maker.sql script in mariaDB, if cannot set up mariadb environement in python
    """
    # (1) Creating mariaDB connection and creating Country, Date, Country_information, Cases_and_death and Hospital_admission tables
    mariadb_connector = MariaDB_Manager("yap", "123qwe", "localhost", 3306, "covid_sea_proj")

    # (2) Create tables
    worldindata_tables = TableBuilder_Worldindata(mariadb_connector)
    worldindata_tables.create_tables()

    # (3) Populate data and country tables to get country_id and date_id 
    worldindata_tuples = Tuple_Generator("[cleaned]-worldindata-covid.csv")
    worldindata_tables.populate_date_table(worldindata_tuples)
    worldindata_tables.populate_country_table(worldindata_tuples)

    # (4) Add date_id and country_id columns to dataframe  
    date_dict = mariadb_connector.map_dates() # date_dict[date]:[date_id]
    map_dict = mariadb_connector.map_countries() # map_dict[country_iso]:[country_id]
    worldindata_tuples.add_date_id_column(date_dict) 
    worldindata_tuples.add_map_id_column(map_dict, "iso_code")
    
    # (5) Populate the remaining tables - Country_information_table, Hospital_admission and Cases_and_death
    worldindata_tables.populate_country_information_table(worldindata_tuples)
    worldindata_tables.populate_hospital_admission_table(worldindata_tuples)
    worldindata_tables.populate_cases_and_death_table(worldindata_tuples)
    
    # Vaccination table 
    vaccination_tables = TableBuilder_Vaccination(mariadb_connector)
    vaccination_tables.create_tables()
    vaccination_tuples = Tuple_Generator("[cleaned]-vaccination-data.csv")
    vaccination_tuples.add_map_id_column(map_dict, "ISO3")
    vaccination_tables.populate_Vaccination_table(vaccination_tuples)
    mariadb_connector.generate_sql_file("db-maker.sql")

if __name__ == "__main__":
    main()


