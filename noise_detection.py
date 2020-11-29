import speech_recognition as sr
from gtts import gTTS
from tkinter import *

a = Tk()
a.title("Intro")
a.geometry("900x600")
a.configure(bg = "black")

def detect_noises():
    r = sr.Recognizer()
    with sr.Microphone() as source :     
        audio = r.listen(source)
        engine = r.recognize_google(audio)
        print(engine)
        noise = gTTS(text = engine, lang='en')
        noise.save("noises.mp3")
        noise.save("noises.wav")
            
Button(a, text = "Detect Noises", font = ("arial",24,"bold"), fg = "dark green", bg = "magenta", command = detect_noises).place(x = 180, y = 380)
a.mainloop()
