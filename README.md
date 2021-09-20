# weather-thing
Easily dump json data from an Ambient Weather station into a sql database.

## Usage
1. Clone the repo 

```git clone https://github.com/benDotDirectory/weather-thing.git ~/weather-thing/```

2. Navigate into the repo and install dependancies

```
cd ~/weather-thing
pip3 install -r requirements.txt
```

3. Create ```.env``` file

```
# weather station
mac_address="WEATHER_STATION_MAC_ADDRESS"
api_key="AMBIENT_WEATHER_API_KEY"
application_key="AMBIENT_WEATHER_APPLICATION_KEY"

# database
db_host="DATABASE_HOST"
db_name="DATABASE_NAME"
db_user="DATABASE_USER"
db_pass="DATABASE_PASSWORD"
db_table="TABLE_NAME"
```

4. Create a DB on your server. (install mariadb, create user, database, and table with schema. configure firewall)

5. Do a test run

```python3 weather.py```

6. Deploy with a task scheduler (I like PM2)

```
npm install -g pm2
pm2 start ~/weather-thing/weather.py --name "weather-thing" --cron "0 * * * *"
```
