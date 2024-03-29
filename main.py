## Import
from dbhandler import DbHandler
import streamlit as st
import requests as req###########
import tools as tool 
import pandas as pd
import random
import os


def forecast_button_status():
    st.session_state.forecast_button_status = not st.session_state.forecast_button_status

def main():
        
    if "forecast_button_status" not in st.session_state:
        st.session_state.forecast_button_status = False
        
    if "days" not in st.session_state:
        st.session_state.days = None


    tool.configure()
    # key_current = os.getenv("key_openweathermap")
    key_forecast = os.getenv("key_weatherbit")
    
    dbhandler = DbHandler("./database.db")

    st.title(":blue[Weather Forecast]")





    cities = dbhandler.execute("SELECT name, country, lat, lon FROM capital_cities;", mode="table")

    cities_df = pd.DataFrame(cities, columns=["city","country","lat","lon"])
    cities_df["options"] = cities_df["city"] + " - " +cities_df["country"]


    selected_city = st.selectbox(
        label="Select a city",
        label_visibility="hidden",
        placeholder="Type or select a city name",
        # index=None,
        options=cities_df["options"]
    )

    search_result = cities_df.loc[cities_df["options"].isin([selected_city])]

    if not search_result.empty:
        lat , lon = search_result["lat"].values[0], search_result["lon"].values[0]
        country_name, city_name = search_result["country"].values[0], search_result["city"].values[0]
    else:
        pass###########







    col1, col2 = st.columns(2)
    with col1:
        current_button = st.button("Current Weather")

    with col2:
        forecast_button = st.button("Forecast", on_click=forecast_button_status)


    st.markdown(
        """
        <style>
            div[data-testid="column"] {
                width: fit-content !important;
                flex: unset;
            }
            div[data-testid="column"] * {
                width: fit-content !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    if current_button:
        forecast_button = False
    elif forecast_button:
        current_button = False

    submit = False

    

    if current_button:

        base_url = "https://api.openweathermap.org/data/2.5/weather"
        parameters = {
            "lat" : lat,
            "lon" : lon,
            "units" : "metric",
            "cnt" : 1,
            "appid": key_current
        }

        submit = True

    elif st.session_state.forecast_button_status:

        st.session_state.days = st.slider(
            min_value=1, 
            max_value=16, 
            value= 1, 
            label= "Forecast for how many days?", 
            label_visibility="hidden"
        )
        
        if st.session_state.days == None:
            st.write("Forecast for how many days?")
        elif st.session_state.days == 1:
            st.write(f"Forecast for tommorow")
        else:
            st.write(f"Forecast for next {st.session_state.days} days")
            
        
        base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
        parameters = {
            "lat" : lat,
            "lon" : lon,
            "units" : "M",
            "key" : key_forecast
        }

        submit = st.button("Ok")



    if submit:

        tool.sleep_timer(0.5, 1)
        weather = tool.request_json(base_url, parameters)
        if not weather:
            st.error("An error occurred.")
        else:
            if current_button:
                # description = weather["weather"][0]["description"]
                temp = weather["main"]["temp"]
                temp_feel = weather["main"]["feels_like"]
                temp_min = weather["main"]["temp_min"]
                temp_max = weather["main"]["temp_max"]
                pressure = weather["main"]["pressure"]
                humidity = weather["main"]["humidity"]
                visibility = weather["visibility"]/1000

            elif forecast_button:
                # description = weather["weather"]["description"]
                weather = weather["data"][st.session_state.days]
                temp = weather["temp"]
                temp_min = weather["min_temp"]
                temp_max = weather["max_temp"]
                temp_feel_min = weather["app_min_temp"]
                temp_feel_max = weather["app_max_temp"]
                pressure = weather["pres"]
                humidity = weather["rh"]
                visibility = weather["vis"]
                temp_feel = (temp_feel_max + temp_feel_min) / 2


            st.write(
                    f"{city_name} in {country_name}:",
                    # description,
                    f"-Temperature: {temp:.0f} Celsius, Can feel like {temp_feel:.0f}",
                    f"-Minimum temp: {temp_min:.0f}",
                    f"-Maximum temp: {temp_max:.0f}",
                    f"-Humidity: {humidity}%",
                    f"-Pressure: {pressure}",
                    f"-Visibility: {visibility:.1f} KM"
            )


if __name__ == "__main__":
    main()


    
    
    
"""

----    

tool.sleep_timer(0.5, 1)
res_w = req.get(url=base_url, params=parameters)

if mode == 1:
    # weather = res_w.json()["main"]
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
        f"{selected_city} in {country_name}:",
        description,
        f"-Temperature: {temp:.0f} Celsius, Can feel like {temp_feel:.0f}",
        f"-Minimum temp: {temp_min:.0f}",
        f"-Maximum temp: {temp_max:.0f}",
        f"-Humidity: {humidity}%",
        f"-Pressure: {pressure}",
        f"-Visibility: {visibility:.1f} KM",
        sep="\n"
)
"""