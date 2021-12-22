from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room
from flask_session import Session
from difflib import SequenceMatcher
from pathlib import Path
from datetime import date,datetime

import json


'''
@author Salman Rakin
'''

count=0
stack=set()
fall_query=""
fall_response=""
async_mode = None

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
Session(app)
socketio = SocketIO(app,manage_session=False, async_mode=async_mode)

users_connected=0
#users_active=0


#CLIENT_ACCESS_TOKEN = '9624c80a372f44aeaf364eab4cc182b0'

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def stat():
    global users_connected
    print("Number of User Connected to our Server:",users_connected)
    print("Number of User Actively Chatting:", len(stack))

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        # print(response.query_result.fulfillment_text)
        # print( type(response.query_result.fulfillment_text))

        return response.query_result.fulfillment_text


@app.route('/')
def chat():
  return render_template('login.html')


@app.route('/chatting')
def login():
  return render_template('chat.html')


@socketio.on('stats',namespace='/chat')
def show_stats():
    emit('server_stats',{'User_Connected': users_connected, 'User_Active': len(stack)},broadcast=False)


@socketio.on('message', namespace='/chat')
def chat_message(message):
  print("message =!! ", message)
  test_message=message
  emit('message', {'data': test_message['data']}, broadcast=False)


@socketio.on('my_conn', namespace='/chat')
def chat_message(data):
    username= data['data']['username']
    mobile_number=data['data']['mobile_number']
    session= data['data']['session']
    date= data['data']['full']
    time= data['data']['time']
    print(" A user named " +username+" with mobile number "+str(mobile_number)+" and session id "+str(session)+" has connceted to the server at "+date+" "+time )


@socketio.on('discon', namespace='/chat')
def chat_message():
    global users_connected
    print('A user disconnected for reloading...')
    users_connected = users_connected - 1
    # users_active=users_active-1
    if stack:
        stack.pop()
    stat()

@socketio.on('auth', namespace='/chat')
def chat_message(data):

    username=data['data']
    #print("username ---",username)
    print("Authentication blcok in the server")
    username='admin'
    password='admin'
    emit('auth',{'username':username,'password':password},broadcast=False)


@socketio.on('transcript', namespace='/chat')
def chat_message(data):

    username=data['data']['username']
    username=str(username).strip()
    mobile_no=data['data']['mobile_number']
    mobile_no=str(mobile_no).strip()
    #print("mobile_no ---",mobile_no.encode('utf-8'))
    session= data['data']['session']
    session=str(session).strip()
    dir_name=data['data']['full']
    dir_name=str(dir_name).strip()
    print("username ---",username.encode('utf-8'))
    print("mobile_no ---",mobile_no.encode('utf-8'))
    print("session ----",session)
    print("Dir_name ---", dir_name)

    file_name=str(dir_name)+".txt"
    file_or_directory=Path("transcripts/"+mobile_no+"/"+username)

    if file_or_directory.exists():
        print(str(mobile_no.encode('utf-8'))+"/"+str(username.encode('utf-8')) + "  directory  exits---")
    else:
        print(str(mobile_no.encode('utf-8'))+"/"+str(username.encode('utf-8')) + "  --directory does not exit. --So Create it")
        file_or_directory.mkdir(parents=True, exist_ok=True)

    fo = open("transcripts/"+mobile_no+"/"+username+"/"+file_name, "ab+")

    my_file = Path("transcripts/"+mobile_no+"/"+username+"/"+ file_name)
    print("File exists:---", my_file.is_file())

    if my_file.is_file():
            fo.write(str.encode("\n\n || Session_ID:- "+str(session)+" ||\n\n"))
            stat()

    fo.close()


@socketio.on('transcript_user', namespace='/chat')
def chat_message(data):
    username = data['data']['author']
    username=str(username).strip()
    mobile_no = data['data']['mobile_no']
    mobile_no=str(mobile_no).strip()
    session = data['data']['Session']
    session=str(session).strip()
    stack.add(session)
    dir_name=data['data']['full']
    dir_name=str(dir_name).strip()
    time=data['data']['time']
    time=str(time).strip()
    query=data['data']['message']
    query=str(query).strip()
    print("username ---", username.encode('utf-8'))
    print("mobile_no --", mobile_no.encode('utf-8'))
    print("session --transcript_user", session)
    print("Dir Name-", dir_name)
    print("Time", time)
    print("query----", query.encode('utf-8'))

    file_name = str(dir_name) + ".txt"

    file_or_directory = Path("transcripts/" + mobile_no + "/" + username)

    if file_or_directory.exists():
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  directory  exits--")
    else:
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  --directory does not exit. --So Create it")
        file_or_directory.mkdir(parents=True, exist_ok=True)

    fo = open("transcripts/" + mobile_no + "/" + username + "/" + file_name, "ab+")
    my_file = Path("transcripts/" + mobile_no + "/" + username + "/" + file_name)
    print("File exists:---", my_file.is_file())

    if my_file.is_file():
        fo.write(str.encode("\n\n       ")+username.encode('utf-8')+str.encode("  ( ")+time.encode('utf-8')+str.encode(" ) :-- ") + query.encode('utf-8') + str.encode(" \n\n"))

    fo.close()
    stat()

@socketio.on('transcript_bot', namespace='/chat')
def chat_message(data):
    username = data['data']['author']
    username=str(username).strip()
    mobile_no = data['data']['mobile_no']
    mobile_no=str(mobile_no).strip()
    session = data['data']['Session']
    session=str(session).strip()
    dir_name=data['data']['full']
    dir_name=str(dir_name).strip()
    time=data['data']['time']
    time=str(time).strip()
    query=data['data']['message']
    query=str(query).strip()
    print("username ---", username.encode('utf-8'))
    print("mobile_no --", mobile_no.encode('utf-8'))
    print("session ----transctip_bot ", session)
    print("Dir Name-", dir_name)
    print("Time", time)
    print("query", query.encode('utf-8'))

    file_name = str(dir_name) + ".txt"

    file_or_directory = Path("transcripts/" + mobile_no + "/" + username)

    if file_or_directory.exists():
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  directory  exits--")
    else:
        print(str(mobile_no.encode('utf-8')) + "/" + str(username.encode('utf-8')) + "  --directory does not exit. --So Create it")
        file_or_directory.mkdir(parents=True, exist_ok=True)

    fo = open("transcripts/" + mobile_no + "/" + username + "/" + file_name, "ab+")

    my_file = Path("transcripts/" + mobile_no + "/" + username + "/" + file_name)
    print("File exists:----", my_file.is_file())

    username="Weather-Agent"
    if my_file.is_file():
        fo.write(str.encode("\n\n       ")+username.encode('utf-8')+str.encode("  ( ")+time.encode('utf-8')+str.encode(" ) :-- ") + query.encode('utf-8') + str.encode(" \n\n"))

    fo.close()
    stat()


@socketio.on('response', namespace='/chat')
def chat_message(message):

      global path_fail

      test_message=message

      query=message['data']['message']
      session_id=message['data']['Session']


      print("\n*************** Query-", query.encode('utf-8')," ---- Username:- ", message['data']['author'].encode('utf-8'), " ----- Session ID:- ", message['data']['Session'],"  ********")

      res=detect_intent_texts(
          "florist-shop-5a5b0", session_id, [query], "en-US"
      )
      response={'data':{'message': res,'author':'Rakin'}}
      response=json.dumps(response)
      response=json.loads(response)

      print(response['data'])

      print("query:-",query," response: = ",res,"session: ",message['data']['Session'])
      emit('response', {'data': response['data']}, broadcast=False)

      if "I am sorry" in res:
          print("Yes....................","session: ",message['data']['Session'])
          today=str(date.today())
          print(str(date.today()))

          path = Path('Fail')

          if path.exists() == False:
              path.mkdir(parents=True, exist_ok=True)

          path_fail = "Fail/"+today+".txt"
          username=message['data']['author']
          time=message['data']['time']
          mobile_no=message['data']['mobile_no']

          fo = open(path_fail, "ab+")

          myfile=Path(path_fail)

          if myfile.is_file():
              fo.write(str.encode("\n\n       ") + username.encode('utf-8')+str.encode(" -- ")+mobile_no.encode('utf-8') + str.encode("  ( ") + time.encode('utf-8') + str.encode(" ) :-- ") + query.encode('utf-8') + str.encode(" \n\n"))
              username="Weather-Agent"
              fo.write(str.encode("\n\n       ") + username.encode('utf-8') + str.encode("  ( ") + time.encode('utf-8') + str.encode(" ) :-- ") + res.encode('utf-8') + str.encode(" \n\n"))

          fo.close()
      else:
          print("No....................","session: ",message['data']['Session'])

      stat()

@socketio.on('connect', namespace='/chat')
def test_connect():
    global users_connected
    users_connected = users_connected + 1
    #emit('my response', {'data': 'Connected', 'count': 0})
    print("A user connected to the server.....")
    stat()

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    global users_connected
    print('A user disconnected from our server...')
    #emit('disconnect',broadcast=False)
    users_connected= users_connected -1
    #users_active=users_active-1
    if stack:
        stack.pop()
    stat()



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5003, debug=True)
    #socketio.run(app,debug=True)