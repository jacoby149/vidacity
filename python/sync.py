import pywinauto
from pywinauto import application
import time
import cv2
import json

from audacity_pipe import *


# TODO move the window to look appealing
# app["Audacity"].move_window(0, 0, 400, 400)
def start():    
    file = open("vidacity_settings.json","r")
    settings = json.load(file)
    app = application.Application(backend="uia")
    audacity_path = settings["audacity_path"]
    app.start(audacity_path)
    app.connect(path=audacity_path)
    Audacity = app['Audacity']
    return app,Audacity

app,Audacity = start()

def get_audacity_objects():
        # get audacity objects
        
        pane1 = Audacity['Selection'].descendants()
        pane2 = Audacity['status_line'].descendants()

        secs, stat = 0, 0
        for i, d in enumerate(pane1):
            if i == 18:
                secs = d
        for i, d in enumerate(pane2):
            if i == 1:
                stat = d
        return secs, stat

secs,stat = get_audacity_objects()

def sync_play(title
              ):
    def parsetime(t='Audio Position 00 h 00 m 00.000 s'):
        l = t.split()
        mstsec = 1000
        mstmin = mstsec*60
        msthr = 60 * mstmin
        try:
            return int(float(l[6])*1000 + int(l[4]*mstmin) + int(l[2]*msthr))
        except:
            return 0

    def import_song(title):
        pipe(title,"import")
    # Implementation

    # TODO make stat into correct units
    import_song(title)

    cap = cv2.VideoCapture(title)
    while True:
        s = parsetime(secs.window_text())
        cap.set(0, s)
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
