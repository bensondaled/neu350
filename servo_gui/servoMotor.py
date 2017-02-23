# -*- coding: utf-8 -*-
"""
This is a GUI built using the tkinter and pySerial modules to interface with
an Arduino running servoControl.ino to move a servo attached to the arduino 

Nikhil Deshmukh 
4/17/2015 

Updated by Talmo Pereira for NEU501B final project
12/24/2015
 
"""

import serial
import serial.tools.list_ports
import time
from Tkinter import *

#### Parameters & Constants ####
scale = 6 # degrees per mm of linear displacement
speedDict = {6:"f",5:"e",4:"d",3:"c",2:"b",1:"a"}
maxSpeed = "f"
retractLength = 2 # 0 to 15
#extendLength = 9  # 0 to 15
repeatDelay = 4000 # ms
arduinoPort = "COM6" # default to use if can't auto-detect
################################


# Detect Arduino port
all_ports = list(serial.tools.list_ports.comports()) # list of a 3-tuple for each port
ports = [(port, desc) for port, desc, hwid in all_ports if "Arduino" in desc]
if len(ports) > 0:
    arduinoPort, arduinoDesc = ports[0]
    print "Detected port: %s (%s)" % (arduinoPort, arduinoDesc)
else:
    print "Could not auto-detect port. Using %s as default." % arduinoPort
    print "Ports:"
    print all_ports

## MAKE SURE THE CORRECT COM PORT IS SELECTED
#PORT = "COM6" #  serial port for arduino uno on windows (changes dynamically) 
ser = serial.Serial(arduinoPort, 9600) # initialize serial port with baud rate 9600 

# Initialize GUI class
class Application(Frame): #create the class for the GUI to run
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid() # create the grid on the GUI for the part to snap onto
        self.create_widgets() #the function to create the GUI parts

    def create_widgets(self): #define all GUI parts
        
        self.label2= Label(self)
        self.label2["text"]="Enter # of Repeats" 
        self.label2.grid(row=2,column=1, sticky=E)       
        
        self.button = Button(self) #create a button
        self.button["text"] = "Reset" #set the original text of the button
        self.button["height"] = 2 #set the height of the button to 2 characters tall
        self.button["width"] = 12 #set the button width to 12 characters wide
        self.button["command"] = self.reset #the function the button will run when pressed
        self.button.grid(row = 4, column = 5) #snap the button to the second row of the grid
        
        self.button2 = Button(self) #create a button
        self.button2["text"] = "Move" #set the original text of the button
        self.button2["height"] = 2 #set the height of the button to 2 characters tall
        self.button2["width"] = 12 #set the button width to 12 characters wide
        self.button2["bg"] = "green"        
        self.button2["command"] = self.move #the function the button will run when pressed
        self.button2.grid(row = 2, column = 5) #snap the button to the second row of the grid
        
        self.button3 = Button(self) #create a button
        self.button3["text"] = "Repeat Move" #set the original text of the button
        self.button3["height"] = 2 #set the height of the button to 2 characters tall
        self.button3["width"] = 12 #set the button width to 12 characters wide
        self.button3["bg"] = "yellow"        
        self.button3["command"] = self.repeat #the function the button will run when pressed
        self.button3.grid(row = 3, column = 5) #snap the button to the second row of the grid
        
        self.testButton = Button(self) #create a button
        self.testButton["text"] = "Oscillate" #set the original text of the button
        self.testButton["height"] = 2 #set the height of the button to 2 characters tall
        self.testButton["width"] = 12 #set the button width to 12 characters wide
        self.testButton["bg"] = "pink"        
        self.testButton["command"] = self.oscillate #the function the button will run when pressed
        self.testButton.grid(row = 1, column = 5) #snap the button to the second row of the grid
        
        self.slider= Scale(self)   
        self.slider["label"] = "Baseline Servo Speed" 
        self.slider["length"] =150 
        self.slider["from_"] = 6 
        self.slider["to"] = 1 
        self.slider.grid(row=1, column = 0)
        self.slider["command"]= self.pack()
        
        self.slider2= Scale(self)   
        self.slider2["label"] = "Total Pushrod Displacement (mm)" 
        self.slider2["length"] =150 
        self.slider2["from_"] = 15  
        self.slider2["to"] = 0 
        self.slider2.grid(row=1, column = 1)
        self.slider2["command"]= self.pack()
        self.slider2.set(2)
        
        self.end = Button(self) #create another button to end the program
        self.end["text"] = "Quit GUI" #set the text on the button
        self.end["height"] = 2 #set the button height to 2 characters
        self.end["width"] = 12 #set the button width to 12 characters
        self.end["bg"] = "red" #set the background color of the button to red
        self.end["command"] = self.quit #the quit function the button will run
        self.end.grid(row = 4, column = 6, sticky = E) #snap the button to the right side of the third row, second column

        # Repeats textbox
        self.ent=Entry(self)
        self.ent.grid(row=2,column=2)
        self.ent["command"]=self.pack()
        self.ent.insert(0, "3") # default
        
        self.labelDur= Label(self)
        self.labelDur["text"]="Exposure duration (s):" 
        self.labelDur.grid(row=1,column=1, sticky=E)

        # Duration textbox
        self.dur=Entry(self)
        self.dur.grid(row=1,column=2)
        self.dur["command"]=self.pack()
        self.dur.insert(0, "5") # default

        # Expose button
        self.exposeBtn = Button(self)
        self.exposeBtn["text"] = "Expose"
        self.exposeBtn["height"] = 2
        self.exposeBtn["width"] = 12
        self.exposeBtn["bg"] = "pink"        
        self.exposeBtn["command"] = self.expose
        self.exposeBtn.grid(row = 1, column = 6)

        # Retract button
        self.retractBtn = Button(self)
        self.retractBtn["text"] = "Retract"
        self.retractBtn["height"] = 2
        self.retractBtn["width"] = 12
        self.retractBtn["bg"] = "pink"        
        self.retractBtn["command"] = self.retract
        self.retractBtn.grid(row = 3, column = 6)

        # Extend button
        self.extendBtn = Button(self)
        self.extendBtn["text"] = "Extend"
        self.extendBtn["height"] = 2
        self.extendBtn["width"] = 12
        self.extendBtn["bg"] = "pink"        
        self.extendBtn["command"] = self.extend
        self.extendBtn.grid(row = 2, column = 6)
        
    def move(self):
        speed = self.slider.get()
        displacement = self.slider2.get()
        ser.write(str(scale*displacement)+speedDict[speed])
        print 'Move: %d, Speed: %s' % (displacement, speed)
        
    def oscillate(self): # goes back and forth
        speed = self.slider.get()
        displacement = self.slider2.get()
        reps = int(self.ent.get())
        duration = float(self.dur.get())
        for i in range(reps):
            print "%d/%d" % (i+1, reps)
            ser.write(str(scale*displacement)+speedDict[speed])
            time.sleep(duration)
            ser.write(str(scale*retractLength)+speedDict[speed])
            time.sleep(duration)

    def extend(self):
        #displacement = extendLength
        displacement = self.slider2.get()
        ser.write(str(scale*displacement)+maxSpeed)
        pass

    def retract(self):
        ser.write(str(scale*retractLength)+maxSpeed)
        pass
            
    def expose(self):
        duration = float(self.dur.get())
        #displacement = extendLength
        displacement = self.slider2.get()
        speed = self.slider.get()

        print "Exposing for: %f secs" % duration
        ser.write(str(scale*displacement)+speedDict[speed])
        time.sleep(duration)
        ser.write(str(scale*retractLength)+speedDict[speed])
        
    def repeat(self):
        reps=int(self.ent.get())
        for i in range(0,reps):
            self.reset()
            self.after(repeatDelay)
            self.move()
            print 'Repeat: %d/%d' % (i+1, reps)
            
    def reset(self): # define the function to reset the servo motor to position 0
        ser.write("r")
        print 'Reset'
        
    def quit(self): #define the function to kill the program
        ser.close() #close the serial communication
        root.destroy() #destroy the GUI


root = Tk() #these three lines start and run the GUI window in a loop
root.title("Servo Motor Controller") #title the GUI window
app = Application(root)
root.mainloop()
