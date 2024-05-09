import requests

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