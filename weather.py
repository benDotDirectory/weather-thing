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

load_dotenv()

# Grab data from weather station
macAddress = os.getenv("mac_address")
apiKey = os.getenv("api_key")
appKey = os.getenv("application_key")

print("Sending request to api.ambientweather.net...")

req = requests.get("https://api.ambientweather.net/v1/devices/" + macAddress + "?apiKey=" + apiKey + "&applicationKey=" + appKey + "&limit=1", verify=False)
if req.status_code == 200:
    print("Got response!")
else:
    print("Error: failed to get response from ambient weather endpoint (Status code: " + req.status_code + ")")
    print("Exiting...")
    sys.exit(1)

# Convert response from a list to json
resp = req.text
resp = resp.replace("[", "", 1)
resp = resp.replace("]", "", 1)

jsonData = json.loads(resp)

# Build sql
sql = "INSERT INTO " + os.getenv("db_table") + " VALUES("
for item in jsonData:
    sql += "'" + str(jsonData[item]) + "', "

sql = sql[:-2] # Remove trailing comma
sql += ");"


# Connect to database
try:
    dbConnection = mariadb.Connect(
        user=os.getenv("db_user"),
        password=os.getenv("db_pass"),
        host=os.getenv("db_host"),
        database=os.getenv("db_name")
    )
except mariadb.Error as err:
    print("Error making connection with mariadb: " + err)
    sys.exit(1)

# Upload data to database
cur = dbConnection.cursor()

cur.execute(
    sql
)

# Done
print("Done")