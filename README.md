# Firebase-WeatherApp-Main
This project aims to fetch, update, and delete weather data using Firebase Functions and the OpenWeatherMap API.

## Folder Structure
```bash
functions/
│
├── __pycache__/
├── venv/
├── Include/
├── Lib/
├── Scripts/
├── .pyenv.cfg
├── .gitignore
├── main.py
├── requirements.txt
├── .firebaserc
├── .gitignore
├── firebase_credentials.json
├── firestore-debug.log
├── firestore.indexes.json
├── firestore.rules
└── ui-debug.log
```
## Description
The project consists of Python scripts running on Firebase Functions to interact with the Firestore database and fetch weather data from the OpenWeatherMap API.

main.py: Contains Firebase Functions to fetch, update, and delete weather data.
requirements.txt: Specifies Python dependencies required for the project.
firebase_credentials.json: JSON file containing Firebase credentials.
.firebaserc: Firebase configuration file.

## Usage
### Fetch and Save Weather Data
Endpoint: /fetch_and_save_weather

Description: Fetches weather data from the OpenWeatherMap API for a given location and saves it to Firestore.

Parameters:
location: The location for which weather data is requested.

Example Usage:
```bash
GET /fetch_and_save_weather?location=London
```
### Update Weather Data
Endpoint: /update_weather

Description: Updates weather data in Firestore for a given location by fetching the latest data from the OpenWeatherMap API.

Parameters:
location: The location for which weather data is to be updated.

Example Usage:
```bash
GET /update_weather?location=New York
```
### Delete Weather Data
Endpoint: /delete_weather

Description: Deletes weather data from Firestore for a given location.

Parameters:
location: The location for which weather data is to be deleted.

Example Usage:
```bash
GET /delete_weather?location=Paris
```
## Firebase Console Setup
Create a new Firebase project in the Firebase Console.
Navigate to the "Project settings" and note down your Firebase project ID.
Enable Firestore in your Firebase project.
Firebase Emulator Setup

Install the Firebase CLI by running:
```bash
npm install -g firebase-tools
```

Log in to Firebase CLI with your Google account:
```bash
firebase login
```
Navigate to the functions directory of your project in the terminal.

Initialize Firebase project:
```bash
firebase init
```
Follow the prompts to select Firebase features (Functions) and choose your Firebase project.

Install Firebase Emulator:
```bash
firebase init emulators
```
Start the Firebase Emulator:
```bash
firebase emulators:start
```
Deploy Firebase Functions:
```bash
firebase deploy --only functions
```
Using Postman
Make sure your Firebase Emulator is running.

Open Postman and import the provided collection file Firebase_Weather.postman_collection.json.

Use the collection endpoints (fetch_and_save_weather, update_weather, delete_weather) with appropriate parameters.

Send requests to test the Firebase Functions locally.
