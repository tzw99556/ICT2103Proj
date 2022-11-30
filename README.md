# Team BCCK - Covid19 SEA Tracker

pip install flask
pip install pymongo
pip install mysql-connector
pip install mysqlclient

Datasets used:
>> worldindata-covid.csv
>> vaccination.csv 

Workflow: 
(1) Ensure datasets (vaccination.csv & worldindata-covid.csv) in current working directory.
(2) Run FileCleaner.py to extract, filter and clean datasets
    >> [cleaned]-vaccination-data.csv and [cleaned]-worldindata-covid.csv files will be genereated
        these files will be used for RDBMS.
    >> [JSON]-[cleaned]-vaccination-data.csv and m[JSON]-[cleaned]-worldindata-data.csv will be generated these files will be used mongoDB.
(3) Enter mariadb console and create 'covid_sea_pro' database, Run create_db.py [Ensure credentials have been changed]
    >> mariadb database will be created. 
    >> db-maker.sql will also be created. db-maker.sql logs all the queries executed in create_db.py.
    >> If create_db.py cannot be executed due to missing libraries, running 'source db-maker.sql' in mariaDB will create the same database as well. 
(4) View generated charts in Flask by running the mariaDB-Flask.py file in [mariaDB-Flask].

For MongoDB:
Assuming steps (1) to (2) above executed successfully.
(1) View generated charts in Flask by running the mongoDB-Flask.py file in [mongoDB-Flask].