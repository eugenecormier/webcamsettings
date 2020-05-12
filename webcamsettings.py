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
    # get data from cli
    for i in v4l2output:
        if i.split()[2][1:-1] == 'bool':
            deviceSettings[i.split()[0]] = [i.split()[2][1:-1], i.split()[4], i.split()[5]]
        elif i.split()[2][1:-1] == 'menu':
            deviceSettings[i.split()[0]] = [i.split()[2][1:-1], i.split()[4], i.split()[5], i.split()[6], i.split()[7]]
        else:
            deviceSettings[i.split()[0]] = [i.split()[2][1:-1], i.split()[4], i.split()[5], i.split()[7], i.split()[8]]
    # set row in frame to 0 to start
    rowvar = 0
    # populate the frame with available settings
    for i in deviceSettings:
        # label
        globals()[i + 'Label'] = Label(subframe, text=i.capitalize().replace('_', ' '))
        globals()[i + 'Label'].grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
        if deviceSettings[i][0] == 'bool':
            # create and set variable
            globals()[i + 'Var'] = IntVar(name=i)
            globals()[i + 'Var'].set(deviceSettings[i][2][6:])
            # create checkbox
            if deviceSettings[i][1][8:] == '0':
                globals()[i + 'Checkbox'] = Checkbutton(subframe, text='(default: Off)', variable = globals()[i + 'Var'], onvalue = 1, offvalue = 0, height=1)
                globals()[i + 'Checkbox'].grid(row=rowvar, column=1, sticky=W)
            else:
                globals()[i + 'Checkbox'] = Checkbutton(subframe, text='(default: On)', variable = globals()[i + 'Var'], onvalue = 1, offvalue = 0, height=1)
                globals()[i + 'Checkbox'].grid(row=rowvar, column=1, sticky=W)
        else:
            # create slider
            # create and set variable
            globals()[i + 'Var'] = IntVar(name=i)
            globals()[i + 'Var'].set(deviceSettings[i][4][6:])
            # create slider
            globals()[i + 'Slider'] = Scale(subframe, variable = globals()[i + 'Var'], from_=deviceSettings[i][1][4:], to=deviceSettings[i][2][4:], length=400, orient=HORIZONTAL)
            globals()[i + 'Slider'].grid(row=rowvar, column=1, sticky=W)
            # tell user defaults
            globals()[i + 'Default'] = Label(subframe, text='(default: ' + deviceSettings[i][3][8:] + ')')
            globals()[i + 'Default'].grid(row=rowvar, column=2, sticky=(W) ,padx=xpadding, pady=ypadding)
        globals()[i + 'Var'].trace('w', change)
        rowvar = rowvar + 1

def change(*args):
    proc = subprocess.run(["v4l2-ctl -d " + devicemenuVar.get() + " -c " + args[0] + "=" + str(globals()[args[0] + 'Var'].get())], shell=True)


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