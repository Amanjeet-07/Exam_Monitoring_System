import tkinter as tk
from tkinter import *
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from tkinter import messagebox
a = Tk()
a.title("Intro")
a.geometry("900x600")
a.configure(bg = "black")
Label(a, text = "Online Examination Module", font = ("arial",30,"bold"), fg = "black", bg = "white").place(x = 200, y = 100)
    
def register():
    reg = Tk()
    reg.title("Register")
    reg.geometry("900x600")
    reg.configure(bg = "black")
      
   
            
    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        faces,Id = getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImageLabel\Trainner.yml")      
        tk.messagebox.showinfo('Congratulations',' You have been registered') 
    
    def getImagesAndLabels(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        faces=[]
        Ids=[]
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            pilImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            imageNp=np.array(pilImage,'uint8')
            #getting the Id from the image
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(Id)        
        return faces, Ids
    
    def clearAll():
        text1.delete(0, END)
        text2.delete(0, END)
    
    def submit():
        pass
    
    Label(reg, text = "Register", font = ("arial",32,"bold"), fg = "dark green", bg = "magenta").place(x = 300, y = 100)
    Label(reg, text = "Name                 :", font = ("arial",16,"bold"), fg = "white", bg = "black").place(x = 220, y = 200)
    Label(reg, text = "Roll No.              :", font = ("arial",16,"bold"), fg = "white", bg = "black").place(x = 220, y = 240)
    Label(reg, text = "Biometric Scan :", font = ("arial",16,"bold"), fg = "white", bg = "black").place(x = 220, y = 280)

    name = StringVar()
    Id = StringVar()

    text1 = Entry(reg, textvariable = name, font = ("arial",16,"bold"), fg = "black", bg = "white")
    text1.place(x = 400, y = 200, height = 25, width = 200)
    def on_change1():
        
        print(text1.get())
        return text1.get()
    
    def on_change2():
        
        print(text2.get())
        return text2.get()
    
    
    text2 = Entry(reg, textvariable = Id, font = ("arial",16,"bold"), fg = "black", bg = "white")
    text2.place(x = 400, y = 240, height = 25, width = 200) 
    Id1= text2.get()
    print(Id1)
    


    def webcam():
        name=on_change1()
        Id=on_change2()
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 60
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        row = [Id, name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        TrainImages()
        
        
    Button(reg, text = "Open WebCam", font = ("arial",14,"bold"), fg = "dark green", bg = "magenta", command = webcam).place(x = 400, y = 280) 
    
    Button(reg, text = "Submit", font = ("arial",24,"bold"), fg = "dark green", bg = "magenta", command = submit).place(x = 350, y = 400)

def start_exam():
    att = Tk()
    att.title("Start Exam")
    att.geometry("900x600")
    att.configure(bg = "black")
    
    def clearAll():
        text1.delete(0, END)
        text2.delete(0, END)
    
    def webcam():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("StudentDetails\StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)    
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    w=Id
                    
                    tt=str(Id)+"-"+aa
                    n=aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                    
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName,index=False)
       
        
            
        
        Label(att, text = aa, font = ("arial",16,"bold"), fg = "black", bg = "white").place(x = 600, y = 200)
        Label(att, text = w, font = ("arial",16,"bold"), fg = "black", bg = "white").place(x = 600, y = 240)
        

        
        tk.messagebox.showinfo('Congratulations,Your attendance has been marked successfully for the day! You can take the test',icon = 'warning')
        
        cam.release()
        cv2.destroyAllWindows()
         
        
    def submit():
        me=webcam()
        print(me)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        video_capture = cv2.VideoCapture(0)
        face=0 
        eye=0
        while True:
            
            _, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if type(faces) == tuple:
                cv2.putText(frame, "Face : NO" ,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,0,255), 2, cv2.LINE_AA) 
                face=face+1
            else:
                 cv2.putText(frame, "Face : YES" ,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,255,0), 2, cv2.LINE_AA) 
                 face=face-1
    
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                if type(eyes) == tuple:
                    cv2.putText(frame, "Eyes : NO" ,(50,75), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (0,0,255), 2, cv2.LINE_AA) 
                    eye=eye+1
                else:
                    cv2.putText(frame, "Eyes : YES" ,(50,75), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (0,255,0), 2, cv2.LINE_AA)
                    eye=eye-1
        
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
            if eye <=30 and face <=200 :
                cv2.imshow('Video', frame)
                print("Eye")
                print(eye)
                print("Face")
                print(face)
            else :
                video_capture.release()
                cv2.destroyAllWindows()
            
                
                
            
            if cv2.waitKey(100) & 0xFF == ord('q'): 
               break

        
    
    Label(att, text = "Attendance", font = ("arial",32,"bold"), fg = "dark green", bg = "magenta").place(x = 260, y = 100)
    Label(att, text = "Biometric Scan :", font = ("arial",16,"bold"), fg = "white", bg = "black").place(x = 150, y = 200)
    Label(att, text = "Name    :", font = ("arial",16,"bold"), fg = "white", bg = "black").place(x = 500, y = 200)
    Label(att, text = "Roll No. :", font = ("arial",16,"bold"), fg = "white", bg = "black").place(x = 500, y = 240)
    
    
    
    Button(att, text = "Open WebCam", font = ("arial",14,"bold"), fg = "dark green", bg = "magenta", command = webcam).place(x = 160, y = 230) 
    
    Button(att, text = "Start Exam", font = ("arial",24,"bold"), fg = "dark green", bg = "magenta", command = submit).place(x = 300, y = 400) 

Button(a, text = "Register", font = ("arial",24,"bold"), fg = "dark green", bg = "magenta", command = register).place(x = 180, y = 380)
Button(a, text = "Start Exam", font = ("arial",24,"bold"), fg = "dark green", bg = "magenta", command = start_exam).place(x = 520, y = 380)

a.mainloop()
