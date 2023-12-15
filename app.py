import random
from threading import Lock, Thread
from flask_socketio import SocketIO
from datetime import datetime
from flask import Flask, render_template, request
import threading

thread_lock = Lock()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'szczery!'
socketio = SocketIO(app, cors_allowed_origins='*')

chart_threads = {}  # Store threads for each chart

class StoppableThread(Thread): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def display_active_threads():
    thread_list = threading.enumerate()
    for thread in thread_list:
        print(thread)
        

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def background_thread_chart(chart_number, sleep_time):
    try:
        print(f"Generation of random values for the chart {chart_number}")
        connected = True
        while connected and not chart_threads[chart_number].stopped():
            data = random.randrange(1, 10**chart_number)
            print(data)
            socketio.emit(f'updateSensorData{chart_number}', {'value': data, "date": get_current_datetime()})
            socketio.sleep(sleep_time)
    except Exception as e:
        print(f"Error in background_thread_chart {chart_number}: {str(e)}")
        chart_threads[chart_number].stop()

def start_chart_threads():
    with thread_lock:
        for chart_number in range(1, 4):
            if chart_number not in chart_threads or not chart_threads[chart_number].is_alive():
                chart_threads[chart_number] = StoppableThread(target=background_thread_chart, args=(chart_number, 0.5))
                chart_threads[chart_number].daemon = True
                chart_threads[chart_number].start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    
    print('Client connected')
    display_active_threads()
    start_chart_threads()
    on_reconnect()

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)
    # Oznacz wątki jako zatrzymane
    for chart_number in chart_threads:
        chart_threads[chart_number].stop()

@socketio.on('reconnect')
def on_reconnect():
    print('Client reconnected')
    # Upewnij się, że wątki są zatrzymane przed ich ponownym uruchomieniem
    for chart_number in chart_threads:
        chart_threads[chart_number].stop()
        chart_threads[chart_number].join()  # Poczekaj na zakończenie wątku
    start_chart_threads()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)

