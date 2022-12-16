import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
import requests, json
import pyrebase

#Configure and Connext to Firebase

firebaseConfig = {'apiKey': "AIzaSyCXlq5A74zvInW9V70glrzbB8HqhjFfOSU",
                  'authDomain': "spry-notch-364712.firebaseapp.com",
                  'databaseURL': "https://spry-notch-364712.firebaseio.com",
                  'projectId': "spry-notch-364712",
                  'storageBucket': "spry-notch-364712.appspot.com",
                  'messagingSenderId': "903481717172",
                  'appId': "1:903481717172:web:8fef7e9081decff89542e1"}

hash_config =  {'algorithm': "SCRYPT",
                'base64_signer_key': "JVwQhI8DnfoEBmsBv6nWpMPn17zQqX+ofwG5MUK64KNO0SWCDU8c3xUWCKRdfQ9JJpPiLXJkUy30VH0K5+fMHQ==",
                'base64_salt_separator': "Bw==",
                'rounds': "8",
                'mem_cost': "14"
                }

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/add', methods = ['POST'])
def create():
    try:
        data=request.json
        user_Ref.document(str(data['id'])).set(request.json)
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error Occured: {e}"


@userAPI.route('/list')
def read():
    try:
        all_users = [doc.to_dict() for doc in user_Ref.stream()] 
        return jsonify(all_users), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@userAPI.route('/bye/<id>', methods=['GET', 'DELETE'])
def delete(id):
    try:
        user_Ref.document(id).delete()
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error Occured: {e}"




@userAPI.route('/addCity', methods = ['POST'])
def createCity():
    try:
        data=request.json
        user_Ref.document(str(data['city'])).set(request.json)
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error Occured: {e}"

@userAPI.route('/temp/<city>')
def temperature(city):
    try:
        city_info = user_Ref.document(city).get().to_dict()
        lat = city_info['lat']
        long = city_info['long']
        temp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_180m&current_weather=true&start_date=2022-12-11&end_date=2022-12-11")
        contents = json.loads(temp.text)
        max_temp = max(contents['hourly']['temperature_180m'])
        min_temp = min(contents['hourly']['temperature_180m'])
        current_temp = contents['current_weather']['temperature']
        s = f"Today's forecast:\n\nCurrent temperature: {current_temp} \nMax temperature: {max_temp} \nMin temperature: {min_temp}"
        return s, 200
    except Exception as e:
        return f"An Error Occured: {e}"


@userAPI.route('/wind/<city>')
def wind_speed(city):
    try:
        city_info = user_Ref.document(city).get().to_dict()
        lat = city_info['lat']
        long = city_info['long']
        temp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=windspeed_180m,winddirection_180m&current_weather=true&start_date=2022-12-11&end_date=2022-12-11")
        contents = json.loads(temp.text)
        max_wind = max(contents['hourly']['windspeed_180m'])
        min_wind = min(contents['hourly']['windspeed_180m'])
        current_wind = contents['current_weather']['windspeed']
        s = f"Today's forecast:\n\nCurrent windspeed: {current_wind} \nMax windspeed: {max_wind} \nMin windspeed: {min_wind}"
        return s, 200
    except Exception as e:
        return f"An Error Occured: {e}"


@userAPI.route('/shouldIGoOut/<city>')
def smart_assist(city):
    try:
        city_info = user_Ref.document(city).get().to_dict()
        lat = city_info['lat']
        long = city_info['long']
        temp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=windspeed_180m,winddirection_180m&current_weather=true&start_date=2022-12-11&end_date=2022-12-11")
        contents = json.loads(temp.text)
        current_wind = contents['current_weather']['windspeed']
        current_temp = contents['current_weather']['temperature']

        
        
        temp_ok = "The temperature is not ideal today, maybe tomorrow!" if current_temp <10 or current_temp > 30 else "Perfect day to go out for an adventure!"
        wind_ok = "You'll enjoy a nice breeze today!" if current_wind <15 else "Too windy, better stay indoors!"

        
        s = f"Today's forecast:\n\n{temp_ok} \n{wind_ok}"
        return s, 200
    except Exception as e:
        return f"An Error Occured: {e}"


@userAPI.route('/auth')
def user_auth():
    try:
        data=request.json
        email = data['email']
        password = data['password']

        def login():
            print("Log in...")
            try:
                login = auth.sign_in_with_email_and_password(email, password)
                print("Successfully logged in!")
                email1 = auth.get_account_info(login['idToken'])['users'][0]['email']
                print(email1)
            except Exception as e:
                print(f"Invalid email or password")

        def signup():
            print("Sign up...")
            try:
                user = auth.create_user_with_email_and_password(email, password)
                print("Successfully signed up!")
            except: 
                print("Email already exists")

        if (data['existing']=="True"):
            login()
        else:
            signup()
        
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error Occured: {e}"