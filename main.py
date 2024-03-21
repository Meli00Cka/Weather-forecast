# Import
import sqlite3
import requests as req
import functions as fu


def main():
    
    # Input
    city = input("Please enter the capital city name: ").title().strip()
    
    
    
    # sql
    conn_str = "./database/database.db"
    qry_select_ll = f"SELECT lat, lon, country FROM capital_cities WHERE name = '{city}';"
    
    with sqlite3.connect(conn_str) as conn_obj:
        cursor = conn_obj.cursor()
        cursor.execute(qry_select_ll)
        data = cursor.fetchone()
        
    country = data[2]



    # API
    url_forecast = "https://api.weatherbit.io/v2.0/forecast/daily"
    key_forecast = "4dbe3926100242cb800545de364dc00c"
    
    url_current = "https://api.openweathermap.org/data/2.5/weather"
    key_current = "426d750d25e7809e465e069a4b6fac55"
    
    
    # Select mode Current/Forecast (by user)
    while True:
        
        ## Input
        mode = fu.user_input_code("Please select a mode:\n[1] for Current weather\n[2] for Forecast")

        ## mode 1 -> Current
        if mode == 1:
            base_url = url_current
            parameters = {
                "lat" : data[0],
                "lon" : data[1],
                "units" : "metric",
                "cnt" : 1,
                "appid": key_current
            }
            break
        
        ## mode 2 -> Forecast
        elif mode == 2:
            base_url = url_forecast
            parameters = {
                "lat" : data[0],
                "lon" : data[1],
                "units" : "M",
                "key" : key_forecast
            }
            
            ### Get the wanted day (by user)
            while True:
                
                ## Input
                days = fu.user_input_code("Forecast for how many days? (maximum 16-days)")
                
                if 0 >= days or days > 16:
                    fu.error_msg("Number can't be less than 1 or above 16")
                    continue
                else:
                    break
                
            break
        
        ## Handle out of range inputs
        else:
            fu.error_msg("this number is not on the list")
            continue
        
        
        
    # request from API
    fu.sleep_timer(0.5, 1)
    res_w = req.get(url=base_url, params=parameters)



    if mode == 1:
        weather = res_w.json()["main"]

        description = res_w.json()["weather"][0]["description"]
        temp = weather["temp"]
        temp_feel = weather["feels_like"]
        temp_min = weather["temp_min"]
        temp_max = weather["temp_max"]

        pressure = weather["pressure"]
        humidity = weather["humidity"]
        visibility = res_w.json()["visibility"]/1000
        
        title = f"-Current weather-"


    elif mode == 2:
        weather = res_w.json()["data"][days-1]

        temp = weather["temp"]
        temp_min = weather["min_temp"]
        temp_max = weather["max_temp"]
        temp_feel_min = weather["app_min_temp"]
        temp_feel_max = weather["app_max_temp"]
        pressure = weather["pres"]
        humidity = weather["rh"]
        visibility = weather["vis"]
        temp_feel = (temp_feel_max + temp_feel_min) / 2
        description = weather["weather"]["description"]

        ## output
        if days == 1:
            title = f"Forecast for tommorrow"
        else:
            title = f"-Forecast for next {days} days-"

    #output
    print(
            title,
            f"{city} in {country}:",
            description,
            f"-Temperature: {temp:.0f} Celsius, Can feel like {temp_feel:.0f}",
            f"-Minimum temp: {temp_min:.0f}",
            f"-Maximum temp: {temp_max:.0f}",
            f"-Humidity: {humidity}%",
            f"-Pressure: {pressure}",
            f"-Visibility: {visibility:.1f} KM",
            sep="\n"
        )


      
main()