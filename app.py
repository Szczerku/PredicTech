import random
from threading import Lock
from flask_socketio import SocketIO
from datetime import datetime
from flask import Flask, render_template, request
import mysql.connector

thread_lock = Lock()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'szczery!'
socketio = SocketIO(app, cors_allowed_origins='*')

def fetch_data_from_database():
    connection = mysql.connector.connect(
        host='192.168.1.15',
        user='szczery',
        password='Allegro123@',
        database='twoja_nowa_baza'
    )

    cursor = connection.cursor()
    cursor.execute('SELECT random_number FROM your_table ORDER BY id DESC LIMIT 1')
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return [item[0] for item in data] if data else None

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def background_thread(chart_id):
    print(f"Generowanie losowych wartości dla wykresu {chart_id}")
    while True:
        dummy_sensor_value = fetch_data_from_database()[0]
        socketio.emit(f'updateSensorData{chart_id}', {'value': dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)

@app.route('/')
def index():
    return render_template('home.html')

@socketio.on('connect')
def connect():
    print('Klient połączony')
    with thread_lock:
        for i in range(1, 4): 
            socketio.start_background_task(background_thread, i)

@socketio.on('disconnect')
def disconnect():
    print('Klient rozłączony',  request.sid)

if __name__ == '__main__':
    socketio.run(app)
