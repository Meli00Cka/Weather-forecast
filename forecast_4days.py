# Import
import sqlite3
import requests as req
import functions as fu

def main():
    # Input
    city = input("Please enter the city name: ").title().strip()

    
    # sql
    conn_str = "./database/database.db"
    qry_select_ll = f"SELECT lat, lon, country FROM capital_cities WHERE name = '{city}';"
    
    with sqlite3.connect(conn_str) as conn_obj:
        cursor = conn_obj.cursor()
        cursor.execute(qry_select_ll)
        data = cursor.fetchone()
        
    country = data[2]


    # getting weather (for next 4 days)
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    parameters = {
        "lat" : data[0],
        "lon" : data[1],
        "appid":"426d750d25e7809e465e069a4b6fac55"
    }

    fu.sleep_timer(0.5, 1)
    res_w = req.get(url=base_url, params=parameters)
    
    # taking the data
    temp = fu.weather_convertor(res_w.json()["main"]["temp"])
    temp_feel = fu.weather_convertor(res_w.json()["main"]["feels_like"])
    temp_min = fu.weather_convertor(res_w.json()["main"]["temp_min"])
    temp_max = fu.weather_convertor(res_w.json()["main"]["temp_max"])

    pressure = res_w.json()["main"]["pressure"]
    humidity = res_w.json()["main"]["humidity"]
    visibility = res_w.json()["visibility"]

    #output
    print(f"{city} in {country}:\n\
    -Temperature: {temp:.1f} Celsius, Feels like {temp_feel:.0f}\n\
    -Minimum temp: {temp_min:.1f}\n\
    -Maximum temp: {temp_max:.1f}\n\
    -Humidity: {humidity}%\n\
    -Pressure: {pressure}\n\
    -Visibility: {visibility}")
    
main()