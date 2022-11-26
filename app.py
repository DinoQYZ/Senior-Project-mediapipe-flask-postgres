from datetime import datetime
import logging

from flask import Flask, Response, redirect, render_template, url_for, request

from camera import *
from dbFunc import *
from table import *
from dateSelect import *

# connect db
cursor, conn = connDB({
    'host':'192.168.56.1', 
    'dbname':'dino', 
    'user':'dino', 
    'password':'dinopwd', 
    'sslmode':'disable'
})

# initial create table if not exist
setupTables(cursor, conn)

# var setup
currentAction = ''
loginStats = getLoginStats(cursor)[0]
dateRange = {
    'start' : {'year':0, 'month':0, 'day':0},
    'end' : {'year':0, 'month':0, 'day':0}
}
dateRangeSeleted = False

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '#$%^&*'

# default page
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

# user page
@app.route('/profile')
def profile():
    if loginStats[0] == True:
        return render_template('profile.html', loginStats=loginStats)
    return redirect(url_for('login'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        USERNAME = request.values['username']
        PASSWORD = request.values['password']
        result, logMsg = userLogin(cursor, USERNAME, PASSWORD)
        if logMsg == '':
            changeLoginStats(True, result[0][1])
            return redirect(url_for('profile'))
        else:
            logging.info(logMsg)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='POST':
        USERNAME = request.values['username']
        PASSWORD = request.values['password']
        PASSWORD_R = request.values['password_r']
        logMsg = userRegister(cursor, USERNAME, PASSWORD, PASSWORD_R)
        if logMsg == '':
            return redirect(url_for('login'))
        else:
            logging.info(logMsg)

    return render_template('register.html')

@app.route('/logout')
def logout():
    changeLoginStats(False, '')
    return redirect(url_for('profile'))

@app.route('/deleteAccount')
def deleteAccount():
    print('to-do')

# profile
@app.route('/profile/myrecord', methods=['GET', 'POST'])
def profile_myrecord():
    record = getRecordByAccount(loginStats, cursor)
    dateRangeSeleted = False
    if request.method =='POST':
        dateRange['start']['year'] = request.values['start_y']
        dateRange['start']['month'] = request.values['start_m']
        dateRange['start']['day'] = request.values['start_d']
        dateRange['end']['year'] = request.values['end_y']
        dateRange['end']['month'] = request.values['end_m']
        dateRange['end']['day'] = request.values['end_d']
        dateRangeSeleted = True

    return render_template('profile_myrecord.html', loginStats=loginStats, record=record, dateRange=dateRange, dateRangeSeleted=dateRangeSeleted)

# change login stats
def changeLoginStats(loggedin, username):
    loginStats[0] = loggedin
    loginStats[1] = username
    updateLoginStats(loginStats, cursor, conn)

# action list page
@app.route('/action')
def action():
    if loginStats[1] != '':
        # check if counter not 0 then insert record
        stats = getStats()
        if stats['counter_L']!=0 or stats['counter_R']!=0:

            # insert record to db
            insertActionCompleted(conn, cursor, {
                'username':loginStats['username'],
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