from flask import Flask, render_template, Response, redirect, url_for
import mediapipe as mp
from datetime import datetime

from dbFunc import *
from camera import *
from login import *

# var setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
currentAction = ''

# connect db
conInfo = {
    'host':'192.168.56.1', 
    'dbname':'dino', 
    'user':'dino', 
    'password':'dinopwd', 
    'sslmode':'disable'
    }
cursor, conn = connDB(conInfo)

# login
loginstats = initLoginStats()

# Flask app
app = Flask(__name__)

# default page
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

# user page
@app.route('/profile')
def profile():
    if loginstats['loggedin'] == True:
        return render_template('profile.html')
    return redirect(url_for('login'))
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
   print('not done')

# action list page
@app.route('/action')
def action():
    # check if counter not 0 then insert record
    stats = getStats()
    if stats['counter_L']!=0 or stats['counter_R']!=0:

        # insert record to db
        insertActionCompleted(conn, cursor, {
            'action':currentAction,
            'reps_l':stats['counter_L'],
            'reps_r':stats['counter_R'],
            'time':str(datetime.now())[:19]
        })
        
        # clear stats
        clearStats()
    return render_template('action.html')

# all action pages
@app.route('/action/biceps_curl', methods=['POST', 'GET'])
def action_biceps_curl():
    return render_template('action/biceps_curl.html')

@app.route('/action/squat', methods=['POST', 'GET'])
def action_squat():
    return render_template('action/squat.html')

@app.route('/action/shoulder_press', methods=['POST', 'GET'])
def action_shoulder_press():
    return render_template('action/shoulder_press.html')

@app.route('/action/lateral_raise', methods=['POST', 'GET'])
def action_lateral_raise():
    return render_template('action/lateral_raise.html')

# set current action
def setCurrentAction(actionName):
    global currentAction
    currentAction = actionName

# generate camara
def gen(camera, function):
    setCurrentAction(function.__name__)
    while True:
        global frame
        frame=camera.get_frame(function)
        yield(b'--frame\r\n' b'Content-Type:  image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# each camera of action
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

# run
if __name__=="__main__":
    app.run('0.0.0.0', debug=True)