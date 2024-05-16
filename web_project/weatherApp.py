import requests
import json
import re
from datetime import datetime

class WeatherPeriod:
    def __init__(self, number, name, start_time, date, end_time, is_daytime, temperature, temperature_unit, dewpoint, humidity,wind_speed, wind_direction, icon_url, short_forecast, short_description, detailed_forecast, location):
        
        self.number = number
        self.name = name
        self.start_time = start_time
        self.date = date 
        self.end_time = end_time
        self.is_daytime = is_daytime
        self.temperature = temperature
        self.temperature_unit = temperature_unit
        self.dewpoint = dewpoint
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.icon_url = icon_url
        self.short_forecast = short_forecast
        self.short_description = short_description
        self.detailed_forecast = detailed_forecast
        self.location = location

def createShortDescriptions(short_forecast):
    weather_keywords = {
        "Sunny",
        "Clear",
        "Mostly Clear",
        "Partly Cloudy",
        "Mostly Cloudy",
        "Cloudy",
        "Drizzle",
        "Rain",
        "Showers",
        "Thunderstorms",
        "Snow",
        "Wintry Mix",
        "Fog",
        "Mist",
        "Haze",
        "Patchy",
        "Overcast"
    }
        
    short_forecast = short_forecast.lower()
    keywords_found = []
    for keyword in weather_keywords:
            if keyword.lower() in short_forecast:
                keywords_found.append(keyword)
    
    return ', '.join(keywords_found)
    
forecast_iconsDay = {
    "Sunny": "images/weather-icons/sun.png",
    "Clear": "images/weather-icons/sun.png",
    "Mostly Sunny": "images/weather-icons/day-cloudy.png",
    "Partly Cloudy": "images/weather-icons/day-cloudy.png",
    "Mostly Cloudy": "images/weather-icons/cloudy.png",
    "Cloudy": "images/weather-icons/cloudy.png",
    "Foggy": "images/weather-icons/fog.png",
    "Light Rain": "images/weather-icons/day-rain.png",
    "Showers": "images/weather-icons/showers.png",
    "Thunderstorms": "images/weather-icons/day - storm.png",
    "Windy": "images/weather-icons/windy.png",
    "Snow": "images/weather-icons/day snow.png",
    "Wintry Mix": "images/weather-icons/wintry-mix.png",
    "Drizzle": "images/weather-icons/light-rain.png",
    "Patchy Fog": "images/weather-icons/day-fog.png",
    "Hazy": "images/weather-icons/hazy.png"
}

forecast_iconsNight = {
    "Sunny": "images/weather-icons/night.png",
    "Clear": "images/weather-icons/night.png",
    "Mostly Sunny": "images/weather-icons/night-cloudy.png",
    "Partly Cloudy": "images/weather-icons/night-cloudy.png",
    "Mostly Cloudy": "images/weather-icons/cloudy.png",
    "Cloudy": "images/weather-icons/cloudy.png",
    "Foggy": "images/weather-icons/fog.png",
    "Light Rain": "images/weather-icons/night-rain.png",
    "Showers": "images/weather-icons/showers.png",
    "Thunderstorms": "images/weather-icons/night-storm.png",
    "Windy": "images/weather-icons/windy.png",
    "Snow": "images/weather-icons/night-snow.png",
    "Wintry Mix": "images/weather-icons/wintry-mix.png",
    "Drizzle": "images/weather-icons/light-rain.png",
    "Patchy Fog": "images/weather-icons/night-fog.png",
    "Hazy": "images/weather-icons/hazy.png"
}
def iconDecider(shortDescription, isDayTime):
    if isDayTime: 
        forecast_icons = forecast_iconsDay
        print("It is day time!")
    else: 
        forecast_icons = forecast_iconsNight
        print("It is Night time!")

    if shortDescription in forecast_icons:
        return forecast_icons[shortDescription]
    else:
        keywords = []
        for keyword in forecast_icons.keys():
            if keyword.lower() in shortDescription.lower():
                keywords.append(keyword)

        closest_match = max(keywords, key = lambda x: len(x)) #returns length of input
        if closest_match:
            icon_filename = forecast_icons[closest_match]
            print("Closest match found:", closest_match)
            print("Displaying icon:", icon_filename)
        else:
            print("Did not find any matching icons!", shortDescription)
def get_location_options(address, api_key):
   
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':

        location = data['results'][0]['geometry']['location']
        lat, lng = location['lat'], location['lng']


        return lat,lng
    else: 
        print('Error: ', data['status'])
        return None, None
    
def convertToCity(lat,lng, locationAPI):   
        locationURL = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lng}&appid={locationAPI}'
        locationResponse = requests.get(locationURL)
        cityJson = locationResponse.json()

        if json.dumps(cityJson[0]["state"]) != "":
            return json.dumps(cityJson[0]["name"]) +", " + json.dumps(cityJson[0]["state"])
        else:
            return json.dumps(cityJson[0]["name"]) +", " + json.dumps(cityJson[0]["country"])
def selectWeatherOption(forecastType):
        weatherForecastOptions = [
            '"Forecast" ~ forecast for 12h periods over the next seven days',
            '"forecastHourly" ~ forecast for hourly periods over the next seven days',
        ]

        while True:

            counter = 1
            # for element in weatherForecastOptions:
            #     print(counter, element)
            #     counter += 1

            foreCastSelect = 0

            if forecastType == "daily": 
                foreCastSelect = 1
            else: 
                foreCastSelect = 2
            
            try:
                # user_input = int(input("Which would you like to see? : "))
                
                return  int(foreCastSelect)

            except ValueError:
                print("Error: Please enter a valid integer")       

def convertToStandardTime(time):
    # print(time)
    if time and time.strip():
        time = time[11:19]
        try:
            time_obj = datetime.strptime(time, "%H:%M:%S")
            formatted_time = time_obj.strftime("%I %p %S")
            # print("time: ")
            
            formatted_time = formatted_time[0:5]
            if formatted_time[0] == '0':
                    formatted_time = formatted_time[1:5]
                    # print(formatted_time)
            return formatted_time
            
        except ValueError as e:
            print("ValueError:", e)
            return ""
    else:
        return ""
    
def convertToStandardDate(date):
    if date and date.strip():
        date = date[:date.index('T'):]
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A")
            # print(formatted_date)
            return formatted_date
        except ValueError:
            return ""
    else:
        return ""
def loadPeriods(weatherForecast, location):
   


    periods = []
    for currPeriod in weatherForecast["properties"]["periods"]:
        period = WeatherPeriod(
            currPeriod["number"],
            currPeriod["name"],
            convertToStandardTime(currPeriod["startTime"]),
            convertToStandardDate(currPeriod["startTime"]),
            currPeriod["endTime"],
            currPeriod["isDaytime"],
            currPeriod["temperature"],
            currPeriod["temperatureUnit"],
            currPeriod["dewpoint"]["value"],
            currPeriod["relativeHumidity"]["value"],
            currPeriod["windSpeed"],
            currPeriod["windDirection"],
            iconDecider(currPeriod["shortForecast"], currPeriod["isDaytime"]),
            # currPeriod["icon"],
            currPeriod["shortForecast"],
            createShortDescriptions(currPeriod["shortForecast"]),
            currPeriod["detailedForecast"],
            location
        )
        
        

        periods.append(period)
    
    return periods
    
def printPeriods(periods):
    
    for period in periods:
        print("~" * 40)
        print(f"\n{period.name.center(40)}")
        print(f"Temperature: C" + period.temperature_unit + f" | Dewpoint: {str(period.dewpoint)} ")
        print(f"{str(period.detailed_forecast)}")
        print("\n")
        print(f"Daytime or not: " + f"str{period.is_daytime}")
def main(address, forecastType):
    api_key = 'AIzaSyCzNKaGvIkGHx1LwUE32j6ua89fLIkgKPc'
    locationAPI = 'f450fc239c378750d6a35407f853899c'
    while True:


        lat,lng = get_location_options(address, api_key)

        while True:
            if lat is not None and lng is not None: 
                print(f'Latitiude: {lat}, Longitutde: {lng}')

                officeUrl = f'https://api.weather.gov/points/{lat},{lng}'
        
                officeResponse = requests.get(officeUrl)
                officeForecast = officeResponse.json()
                
                officeOptions = [
                officeForecast['properties']['forecast'],
                officeForecast['properties']['forecastHourly']
                ]

                if officeResponse.status_code == 200:
                    officeForecast = officeResponse.json()
                    weatherOption = selectWeatherOption(forecastType)
                    weatherUrl = officeOptions[weatherOption - 1]

            

                    weatherResponse = requests.get(weatherUrl)

                    if weatherResponse.status_code == 200:
                        weatherForecast = weatherResponse.json()
                        json_string = json.dumps(weatherForecast, indent = 4)
                        # print(json_string)
                        location = convertToCity(lat, lng, locationAPI)
                        # if weatherForecast["startTime"]:
                        #     print(weatherForecast["startTime"])
                        #     time = convertToStandardTime(weatherForecast["startTime"])
                        #     date = convertToStandardDate(weatherForecast["startTime"])
                        # print(location)
                        periods = loadPeriods(weatherForecast, location)

                        # printPeriods(periods)
                        return periods

                        
            
                    else: 
                        print(f"Error: Not a valid choice")

                else: 
                    print(f"Error: Unable to fetch office forecast. Status code : {officeResponse.status_code}")
            else:
                print("Error: Unable to fetch location coordinates.")
        
            countinue_or_exit = input("Do you want to continue with the address: {address} (y/n): ")
            if countinue_or_exit != "y":
                 break

if __name__ == "__main__":
    address = input("Please enter your address (EXIT to terminate): ")
    if address.lower() != "exit":
        periods = main(address) 
        
        