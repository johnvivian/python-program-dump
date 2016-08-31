

# NOTE: this example requires PyAudio because it uses the Microphone class
import pyaudio
import speech_recognition as sr
import os
import pyttsx
from subprocess import call
# obtain audio from the microphone
while 1:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("Say something!")
        audio = r.listen(source)

# recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        a=r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + a)
        if a=="what is your name":
            a='my name is Brian'
        if a=='training':
            call('python 6.py')
        if a=='hello':
            a="Hello!,Welcome to St. Joseph's Institute of Technology"
        if a== 'Nelson':
            a='nelson is an idiot'
        if a=='stop':
            engine = pyttsx.init()
            rate = engine.getProperty('rate')
            engine.setProperty('rate', 130)
            engine.say('Bye!! Have a nice day')
            engine.runAndWait()
            break
        if a== 'who is your creator':
            a='I was created by john'
    except sr.UnknownValueError:
        a="please repeat"
    except sr.RequestError as e:
        a="please check the connection you dolt"
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 130)
    engine.say(a)
    engine.runAndWait()
