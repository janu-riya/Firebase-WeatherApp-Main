import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_functions import https_fn

# Initialize Firebase Admin SDK
firebase_credentials_path = os.path.join(os.path.dirname(__file__), '../firebase_credentials.json')
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

@https_fn.on_request()
def fetch_and_save_weather(request):
    try:
        # Extract location parameter from the request URL
        location = request.args.get('location')  # Location parameter

        # Check if location is provided
        if not location:
            return https_fn.Response("Location parameter is required.", status=400)

        # Call the OpenWeatherMap API to get weather data
        api_key = "1f1ceee1ac34f92a66f9d73657705522"  # Replace with your actual OpenWeatherMap API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 response codes

        # Extract weather data from the API response
        weather_data = response.json()
        temperature = weather_data['main']['temp']  # Temperature in Kelvin
        description = weather_data['weather'][0]['description']  # Weather description
        latitude = weather_data['coord']['lat']  # Latitude
        longitude = weather_data['coord']['lon']  # Longitude
        time = weather_data['dt']  # Time in UNIX timestamp format
        # Save weather data to Firestore
        weather_doc_ref = db.collection('weather').document()
        weather_doc_ref.set({
            'location': location,
            'latitude': latitude,
            'longitude': longitude,
            'time': time,
            'temperature': temperature,
            'description': description
        })

        # Prepare response
        response_data = {
           'Added the location data': f"Weather data added in the documents for location '{location}'."
        }
        return https_fn.Response(response_data, content_type='application/json')

    except requests.RequestException as e:
        error_message = f"Failed to fetch weather data: {str(e)}"
        print(error_message)  # Log error message
        return https_fn.Response(error_message, status=500)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)  # Log error message
        return https_fn.Response(error_message, status=500)
    
import requests

@https_fn.on_request()
def update_weather(request):
    try:
        # Extract location parameter from the request URL
        location = request.args.get('location')  # Location parameter

        # Check if location is provided
        if not location:
            return https_fn.Response("Location parameter is required.", status=400)

        # Fetch weather data from the OpenWeatherMap API
        api_key = "1f1ceee1ac34f92a66f9d73657705522"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 response codes

        # Extract weather data from the API response
        weather_data = response.json()
        latitude = weather_data['coord']['lat']  # Latitude
        longitude = weather_data['coord']['lon']  # Longitude
        time = weather_data['dt']  # Time in UNIX timestamp format
        temperature = weather_data['main']['temp']  # Temperature in Kelvin
        description = weather_data['weather'][0]['description']  # Weather description

        # Query Firestore to find documents with the given location
        weather_ref = db.collection('weather').where('location', '==', location).stream()

        # Update weather data for each matching document
        for doc in weather_ref:
            doc.reference.update({
                'latitude': latitude,
                'longitude': longitude,
                'time': time,
                'temperature': temperature,
                'description': description
            })

        # Prepare response
        response_data = {
            'Updated the location data': f"Weather data updated for all documents with location '{location}'."
        }
        return https_fn.Response(response_data, content_type='application/json')

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)  # Log error message
        return https_fn.Response(error_message, status=500)




@https_fn.on_request()
def delete_weather(request):
    try:
        # Extract location parameter from the request URL
        location = request.args.get('location')  # Location parameter

        # Check if location is provided
        if not location:
            return https_fn.Response("Location parameter is required.", status=400)

        # Delete weather data from Firestore
        weather_query = db.collection('weather').where('location', '==', location)
        docs = weather_query.get()

        if not docs:
            return https_fn.Response(f"No weather data found for location: {location}", status=404)

        for doc in docs:
            doc.reference.delete()

        return https_fn.Response(f"Weather data for location {location} deleted successfully!", status=200)

    except Exception as e:
        error_message = f"Failed to delete weather data: {str(e)}"
        print(error_message)  # Log error message
        return https_fn.Response(error_message, status=500)
