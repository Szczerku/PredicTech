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


#data from linux server - testing!! table_1
def fetch_data_from_database1():
    connection = mysql.connector.connect(
    host='192.168.1.15',
    user='szczery',
    password='Allegro123@',
    database='twoja_nowa_baza'
    )
    cursor = connection.cursor()
    cursor.execute('SELECT random_number FROM table_1 ORDER BY id DESC LIMIT 1')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [item[0] for item in data] if data else None

def fetch_data_from_database2():
    connection = mysql.connector.connect(
    host='192.168.1.15',
    user='szczery',
    password='Allegro123@',
    database='twoja_nowa_baza'
    )
    cursor = connection.cursor()
    cursor.execute('SELECT random_number FROM table_2 ORDER BY id DESC LIMIT 1')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [item[0] for item in data] if data else None

def fetch_data_from_database3():
    connection = mysql.connector.connect(
    host='192.168.1.15',
    user='szczery',
    password='Allegro123@',
    database='twoja_nowa_baza'
    )
    cursor = connection.cursor()
    cursor.execute('SELECT random_number FROM table_3 ORDER BY id DESC LIMIT 1')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [item[0] for item in data] if data else None

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def fetch_data_chart_1():
    dummy_sensor_value = fetch_data_from_database1()[0]
    return  dummy_sensor_value

def fetch_data_chart_2():
    dummy_sensor_value = fetch_data_from_database2()[0]
    return  dummy_sensor_value

def fetch_data_chart_3():
    dummy_sensor_value = fetch_data_from_database3()[0]
    return  dummy_sensor_value

def background_thread_chart_1():
    print(f"Generation of random values for the chart {1}")
    while True:
        data = fetch_data_chart_1()
        socketio.emit(f'updateSensorData{1}', {'value': data, "date": get_current_datetime()})
        socketio.sleep(0.2)

def background_thread_chart_2():
    print(f"Generation of random values for the chart {2}")
    while True:
        data = fetch_data_chart_2()
        socketio.emit(f'updateSensorData{2}', {'value': data, "date": get_current_datetime()})
        socketio.sleep(0.2)

def background_thread_chart_3():
    print(f"Generation of random values for the chart {3}")
    while True:
        data = fetch_data_chart_3()
        socketio.emit(f'updateSensorData{3}', {'value': data, "date": get_current_datetime()})
        socketio.sleep(0.2)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print('Client connected')
    with thread_lock:
        socketio.start_background_task(background_thread_chart_1)
        socketio.start_background_task(background_thread_chart_2)
        socketio.start_background_task(background_thread_chart_3)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)
