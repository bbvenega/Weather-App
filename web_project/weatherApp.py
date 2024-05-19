import requests
import json
import re
from datetime import datetime


# The class below contains all the information needed per period loaded in by the National Weather Services API, Google Geolcation API, and a Coordinate to Location API

class WeatherPeriod:
    def __init__(self, number, name, start_time, date, end_time, is_daytime, temperature ,temperature_unit,  temperature_trend, probabilityOfPreciption_Value, dewpointValue, humidityValue,wind_speed, wind_direction, icon_url, short_forecast, short_description, detailed_forecast, location):
        
        self.number = number
        self.name = name
        self.start_time = start_time

        self.date = date 

        self.end_time = end_time
        self.is_daytime = is_daytime
        self.temperature = temperature
        self.temperature_unit = temperature_unit
        self.temperature_trend = temperature_trend
        self.probabilityOfPreciption_Value = probabilityOfPreciption_Value 
        self.dewpointValue = dewpointValue
        self.humidityValue = humidityValue
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.icon_url = icon_url
        self.short_forecast = short_forecast
        self.short_description = short_description
        self.detailed_forecast = detailed_forecast
        self.location = location

#The function below reads in the NWS short description and shortens it further to match to most significant keywords
def createShortDescriptions(short_forecast):

    #Most common, applicable weather conditions:
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
        
    #Converts the NWS forecast into lowercase, and searches for all keywords listed above in the description.
    short_forecast = short_forecast.lower()
    keywords_found = []
    for keyword in weather_keywords:
            if keyword.lower() in short_forecast:
                keywords_found.append(keyword)
    
    return ', '.join(keywords_found)
    
#The map below contains the same keywords above, and connects them to corresponding weather icons (DAYTIME)
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

#The map below contains the same keywords above, and connects them to corresponding weather icons (NIGHTTIME)
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

#The function below determines which icons to use based on the keywords found in the NWS API's short description, and whether it is daytime or not. 
def iconDecider(shortDescription, isDayTime):


    if isDayTime: 
        forecast_icons = forecast_iconsDay
        # print("It is day time!")
    else: 
        forecast_icons = forecast_iconsNight
        # print("It is Night time!")

    #If the shortDescription directly matches one of the map's keys, return that key.
    if shortDescription in forecast_icons:
        # print("Displaying icon:", forecast_icons[shortDescription])
        return forecast_icons[shortDescription]
    
    # If not, searches for keywords that match our map and stores those.
    else:
        keywords = []
        for keyword in forecast_icons.keys():
            if keyword.lower() in shortDescription.lower():
                keywords.append(keyword)

    # The section of code below finds the longest keyword that matches (Longest tends to be more accurate ex: partly cloudy, partly sunny rather than cloudy and sunny)
        closest_match = max(keywords, key = lambda x: len(x)) #returns length of input
        if closest_match:
            icon_filename = forecast_icons[closest_match]
            # print("Closest match found:", closest_match)
            # print("Displaying icon:", icon_filename)
            return forecast_icons[closest_match]
        else:
            print("Did not find any matching icons!", shortDescription)

# The function below takes in the user's input (an address) and returns that locations latitude and longitude
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

# The function below uses openWeatherMap locatio API to convert coordinates into either City, State or City, Country
def convertToCity(lat,lng, locationAPI):   
        locationURL = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lng}&appid={locationAPI}'
        locationResponse = requests.get(locationURL)
        cityJson = locationResponse.json()

        if json.dumps(cityJson[0]["state"]) != "":
            
            return json.dumps(cityJson[0]["name"]).replace('"','') +", " + json.dumps(cityJson[0]["state"]).replace('"','')
        else:
            return json.dumps(cityJson[0]["name"]).replace('"','') +", " + json.dumps(cityJson[0]["country"]).replace('"','')
        

# This function was originally used to allow the user to select hourly and daily forecast. Now the program just runs it twice (CAN OPTIMIZE)
def selectWeatherOption(forecastType):
        weatherForecastOptions = [
            '"Forecast" ~ forecast for 12h periods over the next seven days',
            '"forecastHourly" ~ forecast for hourly periods over the next seven days',
        ]

        while True:

            counter = 1


            foreCastSelect = 0

            if forecastType == "daily": 
                foreCastSelect = 1
            else: 
                foreCastSelect = 2
            
            try:
                return  int(foreCastSelect)

            except ValueError:
                print("Error: Please enter a valid integer")       

# This funciton uses datetime to convert the NWS API's start time to a properly formated time.
def convertToStandardTime(time):
    # print(time)
    if time and time.strip():
        #The 11th through 19th index in the NWS API always represents the time portion (excludes date)
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
# This funciton uses datetime to convert the NWS API's start time to a properly formated date.   
def convertToStandardDate(date):
    if date and date.strip():
        #The NWS API's starttime's date begins before the Capital 'T'
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

# The function below loads each period passed in through the NWS API with the proper attributes using the functions above and reading in json input
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
            currPeriod["temperatureTrend"],
            currPeriod["probabilityOfPrecipitation"]["value"],
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

 # The following function is used to print the periods for debugging purposes   

#The function below prints the period's information: used for debugging
def printPeriods(periods):
    
    for period in periods:
        print("~" * 40)
        print(f"\n{period.name.center(40)}")
        print(f"Temperature: C" + period.temperature_unit + f" | Dewpoint: {str(period.dewpoint)} ")
        print(f"{str(period.detailed_forecast)}")
        print("\n")
        print(f"Daytime or not: " + f"str{period.is_daytime}")

# The following main function runs and loads all of the weather periods based on the user's address
def main(address, forecastType):
    api_key = 'AIzaSyCzNKaGvIkGHx1LwUE32j6ua89fLIkgKPc'
    locationAPI = 'f450fc239c378750d6a35407f853899c'
    while True:


        lat,lng = get_location_options(address, api_key)

        while True:
            if lat is not None and lng is not None: 
                # print(f'Latitiude: {lat}, Longitutde: {lng}')

                # This API call gets the nearest NWS Office Location to the User's address, and converts it to a JSON 
                officeUrl = f'https://api.weather.gov/points/{lat},{lng}'
                officeResponse = requests.get(officeUrl)
                officeForecast = officeResponse.json()
                # print(officeForecast)
                
                # The following dictionary was created to differentiate the hourly and daily forecasts the NWS API provides
                officeOptions = [
                officeForecast['properties']['forecast'],
                officeForecast['properties']['forecastHourly']
                ]

                if officeResponse.status_code == 200:
                    officeForecast = officeResponse.json()
                    weatherOption = selectWeatherOption(forecastType)
                    weatherUrl = officeOptions[weatherOption - 1]

            
                    # For both forecast times, return the respective API call and convert to JSON if succesful
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

                        #Load periods based on input
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
        
        