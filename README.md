

                                            =======================
                                              Smart-Weather-Agent
                                            =======================


# Smart-Weather-Agent


Smart Weather Agent is a NLP based specialized Chatbot for providing weather information for different geographic locations. This application is a python implementation
which actually works as a wrapper over [OpenWeathermapAPI](https://openweathermap.org/api) that stimulates HCI (Human Computer Interaction) in a way that user can interact
with the Agent instead of simply calling the Weather APIs. This application extract the required city from the user query and prepare the request url to call the 
[endpoint](https://openweathermap.org/current) for getting back all the necessary weather parameters as JSON from the API. Finally, based on the response back from the API, 
an NLP based speech has been built to send as the final response to the user with meaningful weather information!!

# Example 
###[Chcek the image...](https://github.com/Rakin061/Smart-Weather-Agent/blob/master/static/Screenshot.png)


        # User: Tell me the weather in Dhaka today  ?
        # Weather-Agent: Today the weather in Dhaka is Haze and the temperature is 22 C. Thanks !!
        # User: What about Tokyo  ?
        # Weather-Agent: Today the weather in Tokyo is clear and the temperature is 5.6 C. Thanks !!
        .............



# Workflow of the Application

Smart-Weather-Agent has been designed as a three tier architecture where this application lies in the first block and flask-socketio has been used to 
communicate with RESTFUL Web Services by flask Request-Response mechanism  

  * [Dialogflow](https://cloud.google.com/dialogflow) is responsible for initializing the NLP services. 
  * Knowledge base has been hosted to [GCP](https://cloud.google.com/)

[WeatherAPI-Python]() (Submodule of this repository) written as a flask web service has been placed in the second tier and acts as a middleware in between Dialogflow 
and OpenWeatherAPI 
  * Communicates with the Dialogflow python client used in the first tier through standard webhook protocol for getting user query. 
  * Extracts required parameter from the user query, prepare request url for calling the OpenWeatherAPI endpoint.
  
Based on the response back from the API with weather data as JSON an NLP based speech has been built to send back to dialogflow as a reply to the user query 
through communicating the flask web service and the dialogflow python client back and forth. All these three tier applications need to work harmonically for 
completing a successful response to a user.



# Functionalities:

1. Realtime Chatting for concurrent distinct users (Session IDs)
2. Get response from the bot across different servers.
3. Support for **Chat Transcripts (Chat History)** added..
4. Login by entering valid Mobile Number and UserName. No authentication needed
5. Conversation Refreshing option
6. Agent will try to keep users in a perfect track with a guided conversation tour but BOT will be capable to answer any open question within the scope.
7. Response generation from linking with databases for some defined questions
8. Inactive session waiting timer and alert and finally auto logout option after a defined inactive period
9. Conversation Archiving and monitoring.
10. Failed Response tracking added..




# Installation:

## Dev Server:

### Clone the Repository:
* `git clone https://github.com/Rakin061/Smart-Weather-Agent.git`

### Initialize and Update the WeatherAPI Submodule
* `git submodule init`
* `git submodule update`

### Create Virtual Environment and install dependencies listed in requirements.txt
* `python3 -m venv virtualenv`
* `source virtualenv/bin/Activate`
* `pip3 install -r requirements.txt`

### Run the Server from terminal or other configuration environment
* `python3 server.py`

### Environment Variable:
* `GOOGLE_APPLICATION_CREDENTIALS=API-Key/florist-shop-5a5b0-93e8784803c8.json`

## Supported Python_Version
Python >= 3.8

### N.B.
* **If error occurred using any socketio dependencies. Just uninstall python-socketio and reinstall it again !!**
* **Add working directory in the configuration otherwise chat history will not be created**

## Uwsgi Server:

* uwsgi --master --https :5003,foobar.crt,foobar.key --http-websockets  --gevent 1000 --wsgi-file server.py --callable app

### It is highly encouraged to run the application in virtual environment. 

# Regards, 

Developer : Salman Rakin

	