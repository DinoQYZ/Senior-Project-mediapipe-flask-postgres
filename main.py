from flask import Flask, render_template, Response
from connect import *
import mediapipe as mp
from camera import *
from datetime import datetime

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
currentAction = ''

conInfo = {'host':'192.168.56.1', 'dbname':'dino', 'user':'dino', 'password':'dinopwd', 'sslmode':'disable'}
cursor, conn = connDB(conInfo)

# Flask app
app = Flask(__name__)

# declare html page
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/action')
def action():
    stats = getStats()
    if stats['counter_L']!=0 or stats['counter_R']!=0:

        # insert record to db
        cursor.execute("""
        INSERT INTO myrecord (action, reps_l, reps_r, time) VALUES (%s, %s, %s, %s);
        """, (currentAction, stats["counter_L"], stats["counter_R"], str(datetime.now())[:19]))

        conn.commit()

        print('currentAction={}, stats:L{} R{}, time:{}'.format(
            currentAction, stats["counter_L"], stats["counter_R"], str(datetime.now())[:19]))
        # clear stats
        clearStats()
    return render_template('action.html')

@app.route('/action/biceps_curl', methods=['POST', 'GET'])
def action_biceps_curl():
    stats = getStats()
    return render_template('action/biceps_curl.html', stats=stats)

@app.route('/action/squat', methods=['POST', 'GET'])
def action_squat():
    stats = getStats()
    return render_template('action/squat.html', stats=stats)

@app.route('/action/shoulder_press', methods=['POST', 'GET'])
def action_shoulder_press():
    stats = getStats()
    return render_template('action/shoulder_press.html', stats=stats)

@app.route('/action/lateral_raise', methods=['POST', 'GET'])
def action_lateral_raise():
    stats = getStats()
    return render_template('action/lateral_raise.html', stats=stats)

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