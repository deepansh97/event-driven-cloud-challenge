import pandas as pd
import json
import boto3
import os
import transform
import sys
import psycopg2
import datetime

rdsEndpoint = os.environ['endpoint']
db_username = os.environ['database']
db_password = os.environ['password']
jh = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
nyt = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
ARN = os.environ['snsARN']



def send_notification(text):
    try:
        sns = boto3.client('sns')
        sns.publish(TopicArn = ARN, Message = text)
    except Exception as e:
        print("Not able to send SMS due to {}".format(e))
        exit(1)
try:
    
    db_connection = psycopg2.connect(database=db_username, user="postgres",password=db_password, host=rdsEndpoint, port="5432")
    print("Connected to database")
except Exception as e:
    send_notification("Unable to connect to database due to {}".format(e))

def lambda_function(event, context):
    
    dfNYT = pd.read_csv(nyt)
    dfJH = pd.read_csv(jh)

    cursor = db_connection.cursor()

    cursor.execute("SELECT to_regclass('test1')")
    table = cursor.fetchall()


    if table[0][0]==None:
        try:
            query = "CREATE TABLE test1 ( Date date PRIMARY KEY,Cases integer, Deaths integer, Recovered integer)"
            cursor.execute(query)
            #print("test1 table created")
        except Exception as e:
            print("table creation failed {}".format(e))
            send_notification("Table Creation Failed {}".format(e))
            exit(1)
            

    try:
        cursor = db_connection.cursor()
        cursor.execute("select count(*) from test1")
        res = cursor.fetchall()
        print("Number of records present in table = ")
        print(res)
        cursor.close()
        max_date = None

        if(res[0][0]==0):
            try:
                fdata = transform.transform_data(dfNYT, dfJH, True, max_date)
            except Exception as e:
                print("Cannot transform data due to {}".format(e))
            
        else:
            cursor = db_connection.cursor()
            cursor.execute("select max(Date) from test1")
            res=cursor.fetchall()[0][0]
            date_max=datetime.datetime.strftime(res,"%Y-%m-%d")
            fdata=transform.transform_data(dfNYT, dfJH, False, max_date)
            
        fdata['date'] = pd.to_datetime(fdata['date'], format='%Y-%m-%d')

    except Exception as e:
        send_notification("Data tranformation is failed {}".format(e))
        #print("Data tranformation is failed due to {}".format(e))
        exit(1)
    cursor = db_connection.cursor()

    try:
        for index in fdata.index:
            #cursor.execute("INSERT into test1(Date, cases, deaths, recovered) values({},{},{},{})".format("'"+str(datetime.date(fdata['Date'][index]))+"'", fdata['cases'][index], fdata['deaths'][index],fdata['Recovered'][index]))
            #cursor.execute("INSERT into test1(Date, cases, deaths, recovered) values({},{},{},{})".format(fdata['Date'][index].to_pydatetime().date(), fdata['Cases'][index], fdata['Deaths'][index],fdata['Recovered'][index]))
            cursor.execute("INSERT into test1(Date, cases, deaths, recovered) values({},{},{},{})".format("'"+str(fdata['date'][index].to_pydatetime().date())+"'", fdata['cases'][index], fdata['deaths'][index],fdata['Recovered'][index]))
        db_connection.commit()

    except Exception as e:
        send_notification("Database insert failed {}".format(e))
        #print("Database insert failed {}".format(e))
        exit(1)

    recordCount = str(len(fdata.index))
    print("Number of records inserted in the table = " +recordCount)
    send_notification("ETL job has completed. Number of records inserted in the table = "+recordCount)

