from flask import Flask, render_template, Response, request
from gym_assistant import *
import mediapipe as mp
from camera_2 import *
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    stats = getStats()
    return render_template('home.html', stats=stats)

def gen(camera):
    # s = request.form['actionChoose']
    while True:
        global frame
        # if s == 'biceps_crul':
        #     frame=camera.get_frame(biceps_curl)
        # elif s == 'squat':
        #     frame=camera.get_frame(squat)
        # elif s == 'shoulder_press':
        #     frame=camera.get_frame(shoulder_press)
        # elif s == 'lateral_raise':
        #     frame=camera.get_frame(lateral_raise)
        frame=camera.get_frame(lateral_raise)
        yield(b'--frame\r\n' b'Content-Type:  image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run('0.0.0.0', debug=True)