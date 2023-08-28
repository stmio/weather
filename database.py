#!/usr/bin/python3
import MySQLdb, datetime, json, os


class mysql_database:
    def __init__(self):
        credentials_file = os.path.join(os.path.dirname(__file__), "credentials.mysql")
        f = open(credentials_file, "r")
        credentials = json.load(f)
        f.close()
        for key, value in credentials.items():  # remove whitespace
            credentials[key] = value.strip()

        self.connection = MySQLdb.connect(
            user=credentials["USERNAME"],
            password=credentials["PASSWORD"],
            database=credentials["DATABASE"],
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=[]):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


class weather_database:
    def __init__(self):
        self.db = mysql_database()
        self.insert_template = "INSERT INTO WEATHER_MEASUREMENT (AMBIENT_TEMPERATURE, GROUND_TEMPERATURE, AIR_QUALITY, AIR_PRESSURE, HUMIDITY, WIND_DIRECTION, WIND_SPEED, WIND_GUST_SPEED, RAINFALL, CREATED) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.update_template = (
            "UPDATE WEATHER_MEASUREMENT SET REMOTE_ID=%s WHERE ID=%s;"
        )
        self.upload_select_template = (
            "SELECT * FROM WEATHER_MEASUREMENT WHERE REMOTE_ID IS NULL;"
        )

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_none(self, val):
        return val if val != None else "NULL"

    def insert(
        self,
        ambient_temperature,
        ground_temperature,
        air_quality,
        air_pressure,
        humidity,
        wind_direction,
        wind_speed,
        wind_gust_speed,
        rainfall,
        created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):
        params = (
            ambient_temperature,
            ground_temperature,
            air_quality,
            air_pressure,
            humidity,
            wind_direction,
            wind_speed,
            wind_gust_speed,
            rainfall,
            created,
        )
        print(self.insert_template % params)
        self.db.execute(self.insert_template, params)
