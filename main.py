from flask import Flask, render_template, Response
from gym_assistant import *
import mediapipe as mp
from camera import *
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    clearStats()
    return render_template('test.html')

@app.route('/home')
def home():
    clearStats()
    return render_template('home.html')

@app.route('/action', methods=['POST', 'GET'])
def action1():
    stats = getStats()
    return render_template('action/action1.html', stats=stats)

@app.route('/action', methods=['POST', 'GET'])
def action2():
    stats = getStats()
    return render_template('action/action2.html', stats=stats)

@app.route('/action', methods=['POST', 'GET'])
def action3():
    stats = getStats()
    return render_template('action/action3.html', stats=stats)

@app.route('/action', methods=['POST', 'GET'])
def action4():
    stats = getStats()
    return render_template('action/action4.html', stats=stats)

def gen(camera, function):
    while True:
        global frame
        frame=camera.get_frame(function)
        yield(b'--frame\r\n' b'Content-Type:  image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video/bisceps_curl')
def video_biceps_curl():
    return Response(gen(Video(), biceps_curl), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video/lateral_raise')
def video_lateral_raise():
    return Response(gen(Video(), lateral_raise), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video/shoulder_press')
def video_shoulder_press():
    return Response(gen(Video(), shoulder_press), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video/squat')
def video_squat():
    return Response(gen(Video(), squat), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run('0.0.0.0', debug=True)