import cv2
#import speech_recognition as sr

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

'''def detect_noises():
    r = sr.Recognizer()
    with sr.Microphone() as source :     
        audio = r.listen(source)
        engine = r.recognize_google(audio)
        
        if(engine):
            cv2.putText(frame, "Noise : YES" ,(50,100), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA) 
        else: 
            cv2.putText(frame, "Noise : NO" ,(50,100), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,255,0), 2, cv2.LINE_AA) '''
            
def detect_student(gray, frame):
    #detect_noises()
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if type(faces) == tuple:
        cv2.putText(frame, "Face : NO" ,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,0,255), 2, cv2.LINE_AA) 
    else:
        cv2.putText(frame, "Face : YES" ,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,255,0), 2, cv2.LINE_AA) 
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        if type(eyes) == tuple:
            cv2.putText(frame, "Eyes : NO" ,(50,75), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA) 
        else:
            cv2.putText(frame, "Eyes : YES" ,(50,75), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,255,0), 2, cv2.LINE_AA) 
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    return frame

video_capture = cv2.VideoCapture(0)
while True:
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canvas = detect_student(gray, frame)
    cv2.imshow('Video', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'): #Press q to quit
        break

video_capture.release()
cv2.destroyAllWindows()
