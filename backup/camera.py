import cv2, sys
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class Video(object):
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360-angle

        return angle 

    def get_point(n):
        if n < 6:
            if n == 1:
                part = mp_pose.PoseLandmark.LEFT_EYE_INNER.value
            if n == 3:
                part = mp_pose.PoseLandmark.LEFT_EYE.value
            if n == 5:
                part = mp_pose.PoseLandmark.LEFT_EYE_OUTER.value
            if n == 2:
                part = mp_pose.PoseLandmark.RIGHT_EYE_INNER.value
            if n == 4:
                part = mp_pose.PoseLandmark.RIGHT_EYE.value
            if n == 6:
                part = mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value

        elif n % 2 == 1:
            if n == 7:
                part = mp_pose.PoseLandmark.LEFT_EAR.value
            if n == 9:
                part = mp_pose.PoseLandmark.MOUTH_LEFT.value
            if n == 11:
                part = mp_pose.PoseLandmark.LEFT_SHOULDER.value
            if n == 13:
                part = mp_pose.PoseLandmark.LEFT_ELBOW.value
            if n == 15:
                part = mp_pose.PoseLandmark.LEFT_WRIST.value
            if n == 17:
                part = mp_pose.PoseLandmark.LEFT_PINKY.value
            if n == 19:
                part = mp_pose.PoseLandmark.LEFT_INDEX.value
            if n == 21:
                part = mp_pose.PoseLandmark.LEFT_THUMB.value
            if n == 23:
                part = mp_pose.PoseLandmark.LEFT_HIP.value
            if n == 25:
                part = mp_pose.PoseLandmark.LEFT_KNEE.value
            if n == 27:
                part = mp_pose.PoseLandmark.LEFT_ANKLE.value
            if n == 29:
                part = mp_pose.PoseLandmark.LEFT_HEEL.value
            if n == 31:
                part = mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value

        else:
            if n == 8:
                part = mp_pose.PoseLandmark.RIGHT_EAR.value
            if n == 10:
                part = mp_pose.PoseLandmark.MOUTH_RIGHT.value
            if n == 12:
                part = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            if n == 14:
                part = mp_pose.PoseLandmark.RIGHT_ELBOW.value
            if n == 16:
                part = mp_pose.PoseLandmark.RIGHT_WRIST.value
            if n == 18:
                part = mp_pose.PoseLandmark.RIGHT_PINKY.value
            if n == 20:
                part = mp_pose.PoseLandmark.RIGHT_INDEX.value
            if n == 22:
                part = mp_pose.PoseLandmark.RIGHT_THUMB.value
            if n == 24:
                part = mp_pose.PoseLandmark.RIGHT_HIP.value
            if n == 26:
                part = mp_pose.PoseLandmark.RIGHT_KNEE.value
            if n == 28:
                part = mp_pose.PoseLandmark.RIGHT_ANKLE.value
            if n == 30:
                part = mp_pose.PoseLandmark.RIGHT_HEEL.value
            if n == 32:
                part = mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value

        return [landmarks[part].x, landmarks[part].y]
        
    def __init__(self):
        self.cap=cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        counter, counter_2 = 0, 0
        stage, stage_2 = None, None
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            _, image = self.cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
          
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                global landmarks
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                p1 = Video.get_point(11)
                p2 = Video.get_point(13)
                p3 = Video.get_point(15)
                
                p1_2 = Video.get_point(12)
                p2_2 = Video.get_point(14)
                p3_2 = Video.get_point(16)
                
                # Calculate angle
                angle = Video.calculate_angle(p1, p2, p3)
                angle_2 = Video.calculate_angle(p1_2, p2_2, p3_2)
                
                # Visualize angle
                cv2.putText(image, str(round(angle, 2)), 
                            tuple(np.multiply(p2, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, str(round(angle_2, 2)), 
                            tuple(np.multiply(p2_2, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Curl counter logic
                angle_high = 160
                angle_low = 30

                if angle > angle_high:
                    stage = "down"
                if angle < angle_low and stage =='down':
                    stage ="up"
                    counter +=1
                    print('Left:', counter)
                    
                if angle_2 > angle_high:
                    stage_2 = "down"
                if angle_2 < angle_low and stage_2 =='down':
                    stage_2 ="up"
                    counter_2 +=1
                    print('Right:', counter_2)
                        
            except Exception as err:
                _, _, ex_tb = sys.exc_info()
                filename = ex_tb.tb_frame.f_code.co_filename
                line_number = ex_tb.tb_lineno
                print('error file:', filename, ', on line', line_number)
                print('>>', err)
                pass
            
            cv2.rectangle(image, (0,0), (250,90), (117,104,109), -1)
            cv2.rectangle(image, (710,0), (960,90), (117,104,109), -1)
            
            # Rep data
            cv2.putText(image, 'REPS', (15,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_2), (10,80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.putText(image, 'REPS', (15+710,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10+710,80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (100,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage_2, 
                        (100,80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.putText(image, 'STAGE', (100+710,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (100+710,80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )

            _, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()