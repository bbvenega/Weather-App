import requests
import json

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
    
def selectWeatherOption():
        weatherForecastOptions = [
            '"Forecast" ~ forecast for 12h periods over the next seven days',
            '"forecastHourly" ~ forecast for hourly periods over the next seven days',
            '"forecastGridData" ~ raw forecast data over the next seven days'
        ]

        counter = 1
        for element in weatherForecastOptions:
         print(counter, element)
         counter += 1
    
        user_input = input("Which would you like to see? : ")
        return  int(user_input)

if __name__ == "__main__":
    api_key = 'AIzaSyCzNKaGvIkGHx1LwUE32j6ua89fLIkgKPc'
    while True:
        address = input("Please enter your address: ")
        lat,lng = get_location_options(address, api_key)


        if lat is not None and lng is not None: 
            print(f'Latitiude: {lat}, Longitutde: {lng}')

            officeUrl = f'https://api.weather.gov/points/{lat},{lng}'
    
            officeResponse = requests.get(officeUrl)
            officeForecast = officeResponse.json()
            
            officeOptions = [
            officeForecast['properties']['forecast'],
            officeForecast['properties']['forecastHourly'],
            officeForecast['properties']['forecastGridData']
            ]

            if officeResponse.status_code == 200:
                officeForecast = officeResponse.json()
                weatherOption = selectWeatherOption()
                weatherUrl = officeOptions[weatherOption - 1]

        

                weatherResponse = requests.get(weatherUrl)

                if weatherResponse.status_code == 200:
                    weatherForecast = weatherResponse.json()
                    json_weather = json.dumps(weatherForecast, indent = 4)
                    print(json_weather)
        
                else: 
                    print(f"Error: Not a valid choice")

            else: 
                print(f"Error: Unable to fetch office forecast. Status code : {officeResponse.status_code}")
        else:
            print("Error: Unable to fetch location coordinates.")
    
        countinue_or_exit = input("Do you want to continue? (y/n): ")
        if countinue_or_exit != "y":
            break
    