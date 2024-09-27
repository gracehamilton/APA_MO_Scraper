import psycopg2

from config import load_sql_config # type: ignore
import pandas as pd
import numpy as np

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def writeToDB(config):
    data = open("gracehamilton.io/dogData.csv", "r")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as curs:
                #doesn't handle nulls for columns very well
                curs.copy_from(data, 'alldata', sep=";", columns =('petfinder_id', 'primary_breed', 'secondary_breed', 'mixed', 'age', 'gender', 'dog_size', 'dog_name', 'description', 'apa_id', 'url', 'photo', 'last_modified', 'created_at'))
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)
    data.close()

if __name__ == '__main__':
    config = load_sql_config()
    writeToDB(config)