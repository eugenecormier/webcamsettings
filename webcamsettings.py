#!/usr/bin/env python3
###################################################
# Imports
###################################################
import subprocess
from tkinter import *
from tkinter import ttk

###################################################
# Initial Variables
###################################################
xpadding=5
ypadding=5

###################################################
# Definitions
###################################################
def createwebcamdevlist():
    webcamdevlist = []
    v4l2rawoutput = subprocess.check_output(['v4l2-ctl', '--list-devices']).decode().splitlines()
    for i in v4l2rawoutput:
        if "/dev/video" in i:
            webcamdevlist.append(i.strip())
    return(webcamdevlist)

###################################################
# Main Window
###################################################
root = Tk()
root.title("Webcam Settings")
mainframe = ttk.Frame(root, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
webcamdevlist = createwebcamdevlist()

# watch for setting changes
def callback(*args):
    print("variable changed!")

# device dropdown menu
rowvar = 0
devicemenuLabel = Label(mainframe, text="Device:")
devicemenuLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
devicemenuVar = StringVar(mainframe)
devicemenuVar.set(webcamdevlist[0])
devicemenuMenu = OptionMenu(mainframe, devicemenuVar, *webcamdevlist)
devicemenuMenu.grid(row=rowvar, column=1, sticky=W)
devicemenuVar.trace('w', callback)
rowvar = rowvar + 1

###################################################
# Main Program
###################################################
root.mainloop()