## Import
from dbhandler import DbHandler
import streamlit as st
import tools as tool 
import pandas as pd

def main():
    
    # setup
    key = st.secrets["key_weatherbit"]
    
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
    
    if "output" not in st.session_state:
        st.session_state.output = ""
        
        
    # streamlit config
    st.set_page_config(
        layout="centered",
        page_title="Weather Forecast", 
        page_icon="https://cdn.weatherbit.io/static/img/icons/c02d.png", 
        initial_sidebar_state="auto", 
        menu_items=None
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
            base_url = "https://api.weatherbit.io/v2.0/current"
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

            submit = st.button("Okay")
        

    # get weather
    if submit:
        
        tool.sleep_timer(0.5, 1)
        parameters = {
            "lat" : lat,
            "lon" : lon,
            "units" : "M",
            "key" : key
        }
        weather = tool.send_request(base_url, parameters)
        
        if not weather:
            st.error("An error occurred.")
        
        # extract data from result and show
        else:
            if current_button:

                st.session_state.output=weather_card(city_name, country_name, weather)
                
            elif st.session_state.forecast_button_status:
                st.session_state.output=weather_card(city_name, country_name, weather, forecast=True, days=st.session_state.days)
            
    st.markdown(st.session_state.output, unsafe_allow_html=True)



def weather_card(city_name, country_name, weather_data, forecast=False, days=0):
    
    if forecast:
        data_json = weather_data["data"][days]
        temp_feel = (data_json["app_max_temp"] + data_json["app_min_temp"]) / 2
    else:
        data_json = weather_data["data"][days]
        temp_feel = data_json["app_temp"]
    
    description = data_json["weather"]["description"]
    temp = data_json["temp"]
    humidity = data_json["rh"]
    pressure = data_json["pres"]
    visibility = data_json["vis"]
    icon = data_json["weather"]["icon"]
    
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
            <img src="https://www.weatherbit.io/static/img/icons/{icon}.png" alt="weather icon" title="{description}">
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
