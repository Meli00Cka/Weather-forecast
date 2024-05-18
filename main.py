## Import
from dbhandler import DbHandler
import streamlit as st
import tools as tool 
import pandas as pd
import os

def main():
    
    # setup
    tool.configure()
    key = os.getenv("key_openweathermap")
    
    dbhandler = DbHandler("./database.db")

    # get capitals
    cities = dbhandler.execute("SELECT name, country, lat, lon FROM capital_cities;", mode="table")
    cities_df = pd.DataFrame(cities, columns=["city","country","lat","lon"])
    cities_df["options"] = cities_df["city"] + " - " +cities_df["country"]

    # session variables
    if "forecast_button_status" not in st.session_state:
        st.session_state.forecast_button_status = False
        
    if "days" not in st.session_state:
        st.session_state.days = None
        
        
    # streamlit config
    st.set_page_config(
        layout="centered"
    )
    
    # load css
    local_css("style.css")
    
    
    # app header
    with st.container(height=150, border=False):
        st.title(":green[Weather Forecast]")
        
    # app body
    with st.container(border=False):
        selected_city = st.selectbox(
            label="Select a city",
            # label_visibility="hidden",
            placeholder="Type or select a city name",
            # index=None,
            options=cities_df["options"]
        )
        col1, col2 = st.columns(2)
        with col1:
            current_button = st.button("Current Weather")
        with col2:
            forecast_button = st.button("Forecast", on_click=forecast_button_status)

    # search the selected city
        search_result = cities_df.loc[cities_df["options"].isin([selected_city])]

        if not search_result.empty:
            lat , lon = search_result["lat"].values[0], search_result["lon"].values[0]
            country_name, city_name = search_result["country"].values[0], search_result["city"].values[0]
        else:
            st.error("Couldent find the city, please select a city from the box")


        if current_button:
            forecast_button = False
        elif forecast_button:
            current_button = False

        submit = False

        # currnet/forecast
        if current_button:
            base_url = "https://api.openweathermap.org/data/2.5/weather"
            submit = True

        elif st.session_state.forecast_button_status:

            st.session_state.days = st.slider(
                min_value=1, 
                max_value=4,
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


            base_url = "https://api.openweathermap.org/data/2.5/forecast"

            submit = st.button("Okay")
        

    # get weather
    if submit:
        
        parameters = {
            "lat" : lat,
            "lon" : lon,
            "units" : "metric",
            "appid" : key
        }
        weather = tool.send_request(base_url, parameters)
        
        if not weather:
            st.error("An error occurred.")
        
        # extract data from result and show
        else:
            if current_button:

                output=weather_card(city_name, country_name, weather)
                
            elif st.session_state.forecast_button_status:
                output=weather_card(city_name, country_name, weather, forecast=True, days=st.session_state.days)
            
            st.markdown(output, unsafe_allow_html=True)

        tool.sleep_timer(0.5, 1)


def weather_card(city_name, country_name, weather_data, forecast=False, days=0):
    
    if forecast:
        data_json = weather_data["list"][days*7]
        
        temp = data_json["main"]["temp"]
        temp_feel = data_json["main"]["feels_like"]
        pressure = data_json["main"]["pressure"]
        humidity = data_json["main"]["humidity"]
        description = data_json["weather"][0]["description"]
        icon = data_json["weather"][0]["icon"]
        visibility = data_json["visibility"]
        
    else:
        data_json = weather_data["main"]
        
        description = weather_data["weather"][0]["description"]
        icon = weather_data["weather"][0]["icon"]
        temp = data_json["temp"]
        temp_feel = data_json["feels_like"]
        humidity = data_json["humidity"]
        pressure = data_json["pressure"]
        visibility = weather_data["visibility"]
    
    
    t_text_color = temperature_hex_color(temp)
    tf_text_color = temperature_hex_color(temp_feel)
    
    output = f"""
    <div class="weather_card">
        <div class="weather_main">
            <p class="font_large">{city_name} in {country_name}</p>
            <div class="font_medium">
                <p>{description}</p>
                <p style='color:{t_text_color};'>{temp:.0f} Celsius</p>
                <p style='color:{tf_text_color};'>Can feel like {temp_feel:.0f}</p>
            </div>
        </div>
        <div class="weather_details">
            <img src="https://openweathermap.org/img/wn/{icon}@2x.png" alt="weather icon" title="{description}">
            <p>Humidity: {humidity}%</p>
            <p>Visibility: {visibility:.1f} KM</p>
            <p>Pressure: {pressure} MB</p>
        </div>
    </div>
    """
    
    return output

    
def temperature_hex_color(temp):
    match temp:
        case temp if temp <= -10:
            return "#3f37c9"
        case temp if  -10 < temp <= 0:
            return "#00b4d8"
        case temp if 0 < temp <= 10:
            return "#71a0ee"
        case temp if 10 < temp <= 15:
            return "#ffbe0b"
        case temp if 15 < temp <= 25:
            return "#ee9b00"
        case temp if 25 < temp <= 30:
            return "#bb3e03"
        case temp if temp >= 30:
            return "#ef233c"
        case _:
            return "inherit"
        

def forecast_button_status():
    st.session_state.forecast_button_status = not st.session_state.forecast_button_status


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        




    
if __name__ == "__main__":
    main()