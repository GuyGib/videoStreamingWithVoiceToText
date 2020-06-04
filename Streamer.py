import threading
import time

import speech_recognition as sr
from flask import Flask, render_template, Response, request, flash, url_for
from camera import VideoCamera

app = Flask(__name__)

helpLines = ""
SendText = ""
class Thread_A(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.r = sr.Recognizer()

    def run(self):
        exitFlag=0
        global safeWord
        global SendText
        global helpLines
        while not exitFlag:
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)
                audioText = self.r.listen(source, phrase_time_limit=1)
                try:
                    textOfClient = self.r.recognize_google(audioText)
                    if safeWord in textOfClient:
                        audioText = self.r.listen(source, phrase_time_limit=3)
                        try:
                            SendText = self.r.recognize_google(audioText)
                            helpLines = SendText
                            time.sleep(1)
                            text()
                        except Exception as e:
                            SendText = None
                except Exception as e:
                    textOfClient = None

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html', myfunction=saveWord)


@app.route('/safeWord')
def saveWord():
    global safeWord
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audioText = r.listen(source, phrase_time_limit=1)
        try:
            safeWord = r.recognize_google(audioText)
        except  Exception as e:
            safeWord = None
    if safeWord != None:
        return render_template('index.html', safe='Is your word is ' + safeWord, myfunction=saveWord, GoIn=True)
    else:
        return render_template('index.html', safe=None, myfunction=saveWord)


@app.route("/Video")
def Video():
    # rendering webpage
    a = Thread_A("A")
    a.start()
    return render_template('Video.html')

@app.route("/text")
def text():
    d={"help":helpLines}
    return render_template('text.html',**d)

def gen(camera):
    global SendText
    while True:
        # get camera frame
        frame = camera.get_frame(SendText)
        yield (b'--frame\r\n'
               b'Content-Type: image\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    frame = gen(VideoCamera())
    return Response(frame,
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def flaskThread():
    app.run(host='127.0.0.1', port='5000', debug=True,use_reloader=True)


if __name__ == '__main__':
    # defining server ip address and port
    flaskThread()
