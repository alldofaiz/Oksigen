from flask import Flask, render_template
from flask_socketio import SocketIO
import firebase_admin
from firebase_admin import credentials, db
from flask import jsonify
import os
from os.path import join, dirname
from dotenv import load_dotenv


app = Flask(__name__)
socketio = SocketIO(app)


cred = credentials.Certificate('path/sensortanila-c451b-firebase-adminsdk-26si3-de2b40add1.json')  # service account key
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sensortanila-c451b-default-rtdb.asia-southeast1.firebasedatabase.app'  # URL Firebase Realtime Database
})


@app.route('/')
def index():
    ref = db.reference('/')  
    data = ref.get()
    suhu = data.get('Suhu')
    tds = data.get('TDS')
    ph = data.get('pH')
    time_now = data.get('time_now')
    return render_template('index.html', suhu=suhu, tds=tds, ph=ph, time_now=time_now)

@app.route('/get_data')
def get_data():
    ref = db.reference('/')
    data = ref.get()
    response_data = {
        'suhu': data.get('Suhu'),
        'TDS': data.get('TDS'),
        'pH': data.get('pH'),
        'time_now': data.get('time_now')
    }
    return jsonify(response_data)



if __name__ == '__main__':
    socketio.run(app)
