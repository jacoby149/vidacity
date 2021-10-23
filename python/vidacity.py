import os
import shutil
import webbrowser
from tkinter import *
from tkinter import Tk
from tkinter import filedialog
import sys
import _thread as thread
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

from audacity_pipe import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ---------Making the Window and Frames----------
root = Tk()  # defining the window and storing in the variable roo7t
frame1 = Frame(root)
menu = Menu(frame1)
root.config(menu=menu)
root.wm_iconbitmap(resource_path('logo.ico'))
root.title("Vidacity")
# ---------Various Functions-------------
root.filename = ""

def openFile():
    import sync
    from sync import sync_play
    root.filename = filedialog.askopenfile().name
    print(root.filename)
    global file_indicator
    file_indicator.text = "ayy"
    thread.start_new_thread(sync_play, tuple([root.filename]))
    
    #change the submenu to exit instead of open file
    global subMenu ,contactMenu,menu
    menu.delete("Media")
    menu.delete("Contact")
    subMenu.delete(0)
    subMenu = create_submenu(exit=True)
    contactMenu = create_contactmenu()


def exit_vidacity():
    try : pipe("","close")
    except:sys.exit()
    sys.exit()
  

def end():
    if root.filename == "": exit_vidacity()
    root.end = True
    pipe(root.filename,"export")
    direc = os.path.dirname(root.filename)
    file = os.path.basename(root.filename)[:-3] + "mp3"
    mp3name = direc + "/macro-output/" + file
    print(mp3name)
    outfile = file[:-4] + "(OUT).mp4"
    outpath = direc + "/" +outfile
    # ... create some concatenated clip
    videoclip = VideoFileClip(root.filename)
    background_music = AudioFileClip(mp3name)
    new_clip = videoclip.set_audio(background_music)
    new_clip.write_videofile(outpath,threads = 4)

    shutil.rmtree(direc+"/macro-output")
    exit_vidacity()

def finish():
    end()


def help():
    webbrowser.open("https://jacobhoffman.tk/vidacity")


def contact():
    webbrowser.open("http://jacobhoffman.tk/vidacity")

regsize = ("Helvetica", "20")
minisize = ("Helvetica","12")

# Editing ...MP4
lastmark = "Select MP4"


# ---------Creating Menus----------
def create_submenu(exit = False):
    global menu
    subMenu = Menu(menu)
    menu.add_cascade(
        label="Media", menu=subMenu
    )  # Cascading Options on the ToolBar Such as: File Edit
    if not exit:
        subMenu.add_command(label="Open File", command=openFile)
        # subMenu.add_separator()
        # subMenu.add_command(label="exit", command=exit)
    else:
        subMenu.add_command(label="Exit Without Saving", command=exit_vidacity)

    return subMenu


subMenu = create_submenu()

def create_contactmenu():
    global menu
    contactMenu = Menu(menu)
    menu.add_cascade(label="Contact", menu=contactMenu)
    contactMenu.add_command(label="Help", command=help)
    contactMenu.add_command(label="Report Error", command=contact)
    return contactMenu

contactMenu = create_contactmenu()

# ---------Creating Tri-color Labels----------
file_indicator = Label(root, text=lastmark, bg="blue",
                       font=regsize, fg="white")
file_indicator.pack(fill=X)

topFrame = Frame(root)  # definig a frame that will contain the Widgets
topFrame.pack()
bottomFrame = Frame(root)  # Similarly, definging the next Frame
bottomFrame.pack(side=BOTTOM)


# ---------Various Buttons----------
button5 = Button(
    topFrame, text="Save and Finish", fg="purple", font=regsize, command=finish
)
button5.pack(side=LEFT, padx=5, pady=20)

# -----------The status Bar--------------
root.screenMessage = StringVar()
label = Message(root, textvariable=root.screenMessage,
                width=200, relief=RAISED)
root.screenMessage.set("Vidacity")
label.pack(side=BOTTOM, fill=X)
root.mainloop()
