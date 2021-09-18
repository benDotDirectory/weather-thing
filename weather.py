"""
weather.py
----------
Quick and dirty solution to grab weather data out of the weather station, parse it, and shove it into a sql db
"""

# Imports & config
import os, sys
from dotenv import load_dotenv
import mariadb
import requests
import json

def main():

    load_dotenv()

    # Grab data from weather station
    macAddress = str(os.getenv("mac_address"))
    apiKey = str(os.getenv("api_key"))
    appKey = str(os.getenv("application_key"))

    print("Connecting to device (mac adress: " + macAddress + ")")

    print("Sending request to api.ambientweather.net...")

    req = requests.get("https://api.ambientweather.net/v1/devices/" + macAddress + "?apiKey=" + apiKey + "&applicationKey=" + appKey + "&limit=1")
    if req.status_code == 200:
        print("Got response!")
    else:
        print("Error: failed to get response from ambient weather endpoint (Status code: " + str(req.status_code) + ")")
        print("Exiting...")
        sys.exit(1)

    # Convert response from a list to json
    print("Generating sql...")
    resp = req.text
    resp = resp.replace("[", "", 1)
    resp = resp.replace("]", "", 1)

    jsonData = json.loads(resp)

    # Build sql
    sql = "INSERT INTO " +  str(os.getenv("db_table")) + " VALUES("
    for item in jsonData:
        sql += "'" + str(jsonData[item]) + "', "

    sql = sql[:-2] # Remove trailing comma
    sql += ");"

    print("Generated sql")
    print(sql)

    # Connect to database
    print("Connecting to database: " + os.getenv("db_name") + "." + os.getenv("db_table") + " as " + os.getenv("db_user") + "@" + os.getenv("db_host"))
    try:
        dbConnection = mariadb.connect(
            user=str(os.getenv("db_user")),
            password=str(os.getenv("db_pass")),
            host=str(os.getenv("db_host")),
            database=str(os.getenv("db_name"))
        )
    except mariadb.Error as err:
        print("Error making connection with mariadb: " + str(err))
        sys.exit(1)

    # Upload data to database
    print("Executing sql")

    cur = dbConnection.cursor()

    try:
            print("Executing...")
            cur.execute(sql)
            dbConnection.commit()
            print("Commited")
    except mariadb.Error as e:
            dbConnection.rollback()
            print("Error: " + str(e))

    print("sql executed")

    # Close
    print("Closing connection")
    dbConnection.close()

    # Done
    print("Done")

if __name__ == "__main__":
    main()
