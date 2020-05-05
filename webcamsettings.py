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
mainframe.grid(row=0, column=0, sticky=(N, W, E, S))

subframe = ttk.Frame(root, padding="0 0 0 0")
subframe.grid(row=1, column=0, sticky=(W, E, S))

webcamdevlist = createwebcamdevlist()

#####################################################################################################################
# Main Function - watch for setting changes
def callback(*args):
    # reset the frame
    for i in subframe.winfo_children():
        i.destroy()
    # grab v4l2 output and output to a dict
    v4l2output = subprocess.check_output(['v4l2-ctl', '-d', devicemenuVar.get(), '--list-ctrls']).strip().decode().splitlines()
    # this breaks out keys and value types and values into a dict
    deviceSettings = {}
    for i in v4l2output:
        if i.find('int') != -1 and i.find('flags') != -1:
            end = i.find('flags')-1
            deviceSettings[i.split()[0]] = ['int', i[i.find('value=') + 6: end]]
        elif i.find('int') != -1 and i.find('flags') == -1:
            end = len(i)
            deviceSettings[i.split()[0]] = ['int', i[i.find('value=') + 6: end]]
        elif i.find('bool') != -1 and i.find('flags') != -1:
            end = i.find('flags')-1
            deviceSettings[i.split()[0]] = ['bool', i[i.find('value=') + 6: end]]
        elif i.find('bool') != -1 and i.find('flags') == -1:
            end = len(i)
            deviceSettings[i.split()[0]] = ['bool', i[i.find('value=') + 6: end]]
        elif i.find('menu') != -1 and i.find('flags') != -1:
            end = i.find('flags')-1
            deviceSettings[i.split()[0]] = ['menu', i[i.find('value=') + 6: end]]
        elif i.find('menu') != -1 and i.find('flags') == -1:
            end = len(i)
            deviceSettings[i.split()[0]] = ['menu', i[i.find('value=') + 6: end]]
        #deviceSettings[i.split()[0]] = ['menu', i[i.find('value=') + 6: end]]
    print(deviceSettings)

    #deviceSettings = [i.split()[0] for i in v4l2output]
    #print(deviceSettings)
    #deviceSettingsTypes = [i.split()[0] for i in v4l2output]
    #print(deviceSettingsTypes)


    # set row in frame to 0 to start
    rowvar = 0
    # populate the frame with available settings
    for i in deviceSettings:
        globals()[i + 'Label'] = Label(subframe, text=i.capitalize().replace('_', ' '))
        globals()[i + 'Label'].grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
        rowvar = rowvar + 1
#####################################################################################################################
# device dropdown menu
rowvar = 0
devicemenuLabel = Label(mainframe, text="Device:")
devicemenuLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
devicemenuVar = StringVar(mainframe)
devicemenuVar.set(webcamdevlist[0])
devicemenuMenu = OptionMenu(mainframe, devicemenuVar, *webcamdevlist)
devicemenuMenu.grid(row=rowvar, column=1, sticky=W)
devicemenuVar.trace('w', callback)

# initial population of frame with settings
callback()

###################################################
# Main Program
###################################################
root.mainloop()