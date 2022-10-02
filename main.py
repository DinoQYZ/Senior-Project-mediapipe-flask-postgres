from flask import Flask, render_template, Response
from gym_assistant import *
import cv2

#Python Flask 入門指南
#https://youtu.be/AiUzsr5JZgQ

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# @app.route('/home')
# def testPrint():
#     data = {'A':30, 'B':90, 'C':75}

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run('0.0.0.0', debug=True)