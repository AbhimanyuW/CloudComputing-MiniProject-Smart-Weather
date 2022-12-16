# Cloud Computing Mini Project - Smart Weather

## Group Members
1. Abhimanyu Wadhwa
2. Chinar Amrutkar
3. Sunrita Sarkar

## About

Smart Weather is a set of REST APIs interacting with the Open Meteo weather API to give weather information about a chosen city. Users can signup for an account, in which passwords are stored using SCRYPT hashing authentication. 

## Architecture

![Smart Weather Architecture](https://github.com/chinar-amrutkar/Cloud-Project/blob/master/Smart%20Weather%20Architecture.drawio.png "Smart Weather Architecture")

## 1. Dynamic REST API

The application that we have created aims to provide sufficient information to the user regarding the weather and conditions of a particular city. We are using ‘Open-Meteo’ API to fetch these weather metrics.

We have implemented all the CRUD operations from a user point of view, and like suggested in the architecture diagram above, we are using Google’s Firebase to persist this information.

We are then displaying this information in the form of a JSON response, using the tool Postman. 



**Create Operation - adds a user to our database** 




```
@userAPI.route('/add', methods = ['POST'])

def create():

    try:

         data=request.json

         user_Ref.document(str(data['id'])).set(request.json)

         return jsonify({"Success": True}), 200

    except Exception as e:

        return f"An error occured: {e}"
```




**Read Operation - lists out all the users**


```
@userAPI.route('/list')

def read():

    try:

        all_users = [doc.to_dict() for doc in user_Ref.stream()]

        return jsonify(all_users), 200

    except Exception as e:

        return f"An Error Occured: {e}"

```



**Update Operation - (Post method can update if resource exists, or create if resource does not exist)**


```
@userAPI.route('/addCity', methods = ['POST'])

def createCity():

    try:

         data=request.json

         user_Ref.document(str(data['city'])).set(request.json)

         return jsonify({"Success": True}), 200

    except Exception as e:

         return f"An error occured: {e}"
```





**Delete Operation -  Deletes an existing city by ID**


```
@userAPI.route('/bye/<id>', methods=['GET', 'DELETE'])

def delete(id):

    try:

        user_Ref.document(id).delete()

        return jsonify({"Success": True}), 200

    except Exception as e:

        return f"An error occured: {e}"
```


## 2. External API

The SmartWeather aims to consolidate information from multiple external sources and provide it to the user in a single call. Now, we have implemented one data source, OpenMeteo and its subsequent public API. This data is collected and pushed to a Firebase, ready to serve to the user.

The user can input a city name, it’s subsequent latitude and longitude and the SmartWeather aims at returning the weather conditions, highest and lowest temperatures in Celsius along with a brief message on what to expect during the day. This App is very handy for onces who only want to check weather conditions of a specific city.

### Check Temperature Statistics in a City

```
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
```

### Check Wind Speed Statistics in a City

```
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
```

### Get Smart Suggestions for today's weather in a City

```
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
```

## 3. Cloud Database

We are using Google's Firebase to store persistent information about users and city properties. 


## 4. Security Measures

### Serving application over HTTPS
Our application supports connection through HTTPS protocol.  The certificate is securely stored on the local machine used to run the code.

```
from api import create_app

app = create_app()

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug = True)
    
```


### User accounts and access management with hash-based authentication
Users can signup and login into their accounts. All user passwords are stored using SCRYPT hashing. User data is stored securely in Firebase Authentication system.

```
hash_config =  {'algorithm': "SCRYPT",
                'base64_signer_key': "JVwQhI8DnfoEBmsBv6nWpMPn17zQqX+ofwG5MUK64KNO0SWCDU8c3xUWCKRdfQ9JJpPiLXJkUy30VH0K5+fMHQ==",
                'base64_salt_separator': "Bw==",
                'rounds': "8",
                'mem_cost': "14"
                }
```




## 5. How to Run

The code can be run simply by running the following in the project folder directory:

```
python3 main.py
```

The sever starts running on the localhost once the command is successfully executed. 

The REST APIs used in the code can be used using Postman. 

Using the application along with Postman can be seen in the video at the top of the README.