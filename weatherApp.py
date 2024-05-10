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
    

if __name__ == "__main__":
    
    address = input("Please enter your address: ")

    api_key = 'AIzaSyCzNKaGvIkGHx1LwUE32j6ua89fLIkgKPc'

    lat,lng = get_location_options(address, api_key)


if lat is not None and lng is not None: 
    print(f'Latitiude: {lat}, Longitutde: {lng}')

    officeUrl = f'https://api.weather.gov/points/{lat},{lng}'
    
    officeResponse = requests.get(officeUrl)

    if officeResponse.status_code == 200:

        officeForecast = officeResponse.json()
        json_string = json.dumps(officeForecast, indent=4)
        print(json_string)


        

        officeOptions = [
            officeForecast['properties']['forecast'],
            officeForecast['properties']['forecastHourly'],
            officeForecast['properties']['forecastGridData']
        ]

        counter = 1
        for element in officeOptions:
         print(counter, element)
         counter += 1

        user_input = input("Which would you like to see? : ")
        selectedWeatherService = int(user_input)
        weatherUrl = officeOptions[selectedWeatherService - 1]

        weatherResponse = requests.get(weatherUrl)

        if(weatherResponse.status_code == 200):

            weatherForecast = weatherResponse.json()
            json_weather = json.dumps(weatherForecast, indent = 4)
            print(json_weather)
        
        else: 
            print(f"Error: Not a valid choice")

    else: 
        print(f"Error: Unable to fetch office forecase. Status code : {officeResponse.status_code}")
    
    
    