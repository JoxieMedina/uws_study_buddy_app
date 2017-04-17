"""
Solution for COMP07027 Coursework 2017
Written by B00319125
2017-04
"""

import os
import sys
import pickle
from random import randrange
from easygui import *
from tkinter import *

# The title, text message and options passed to all EasyGUI windows
# N.B Text is always argument #0, title argument #2, options argument#3 and preselect argument 4
title = "UWS STUDY BUDDY"

# global variable whose keys hold existing request IDs; values are not defined (None)
requests = {}

root = None

class RequestGUI():
    def __init__(self, window, rid, form=None):
        self.window = window
        window.title("UWS STUDY BUDDY")
        if form is None:
            form = {}
        self.L = [] # list of labels
        self.L.append(Label(window, text="Create New Request"))
        self.L[-1].grid(row=1)
        self.L.append(Label(window, text="Request ID: "+rid))
        self.L[-1].grid(row=2)
        # create text fields for names and passwords
        form["firstname"] = StringVar()
        form["lastname"] = StringVar()
        form["password"] = StringVar()
        form["password2"] = StringVar()
        self.T1 = Entry(window, textvariable=form["firstname"])
        self.T2 = Entry(window, textvariable=form["lastname"])
        self.T3 = Entry(window, textvariable=form["password"])#, show=bullet)
        self.T4 = Entry(window, textvariable=form["password2"])#, show=bullet)
        self.T1.insert(0,"Firstname")
        self.T2.insert(0,"Surname")
        self.T3.insert(0,"Password")
        self.T4.insert(0,"Re-enter password")
        # hide password fields after they are changed from initial prompt
        def hidepw(p):
            bullet = "\u2022"
            p.config(show=bullet)
        form["password"].trace("w", lambda name, index, mode, sv=form["password"]: hidepw(self.T3))
        form["password2"].trace("w", lambda name, index, mode, sv=form["password2"]: hidepw(self.T4))
        # place the name and password fields in the form
        self.T1.grid(row=3, column=0, columnspan=2)
        self.T2.grid(row=3, column=2, columnspan=2)
        self.T3.grid(row=4, column=0, columnspan=2)
        self.T4.grid(row=4, column=2, columnspan=2)
        # create predefined, multiple choice fields
        form["loc"] = StringVar()
        form["prog"] = StringVar()
        form["mod"] = StringVar()
        form["year"] = StringVar()
        self.rx1 = ["Campus Location", "Ayr", "Dumfries", "Paisley", "Hamilton"]
        self.rx2 = ["Programme", "BSc Computer Science", "BSc Networking", "BSc Multimedia",
            "BSc Computer Games Development", "BSc Business Technology"]
        self.rx3 = ["Module", "Introduction to programming", "Computing systems",
            "Introduction to networks", "Mathematics for computing",
            "Introduction to Web Development", "Professional Development",
            "Computing/Business Technology/Enterprise"]
        self.rx4 = ["Year of Study", "year 1", "year 2", "year 3", "year 4"]
        self.M1 = OptionMenu(window,form["loc"],*self.rx1)
        self.M2 = OptionMenu(window,form["prog"],*self.rx2)
        self.M3 = OptionMenu(window,form["mod"],*self.rx3)
        self.M4 = OptionMenu(window,form["year"],*self.rx4)
        self.M1.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.M2.grid(row=5, column=2, columnspan=2, sticky="ew")
        self.M3.grid(row=6, column=0, columnspan=2, sticky="ew")
        self.M4.grid(row=6, column=2, columnspan=2, sticky="ew")
        form["loc"].set(self.rx1[0])
        form["prog"].set(self.rx2[0])
        form["mod"].set(self.rx3[0])
        form["year"].set(self.rx4[0])
        # create checkboxes (and associated variables) for availability
        self.L.append(Label(window, text="Availability:"))
        self.L[-1].grid(row=7, column=0, sticky="w")
        self.times = ["Morning", "Afternoon", "Evening"]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.timeBoxes = []
        form["timeVars"] = []
        for i in range(7):
            form["timeVars"].append([])
            self.timeBoxes.append([])
            self.L.append(Label(window, text=self.days[i]))
            self.L[-1].grid(row=8+i, column=0, sticky="e")
            for j in range(3):
                if i==0:
                    self.L.append(Label(window, text=self.times[j]))
                    self.L[-1].grid(row=7, column=1+j)
                form["timeVars"][i].append(IntVar())
                form["timeVars"][i][j].set(0)
                self.timeBoxes[i].append(Checkbutton(window, variable=form["timeVars"][i][j]))
                self.timeBoxes[i][j].grid(row=8+i, column=1+j)

class Request:
    def __init__(self, requestid):
        global requests, root
        requestid = str(requestid)
        self.requestid = requestid
        self.form = {}
        gui = RequestGUI(root, requestid, self.form)
        root.mainloop()
        msg = "Please VERIFY Your Request Information\n" + \
            "(or edit for testing purposes only):"
        title = "Request Info"
        fieldNames = ["Firstname", "Surname",
            "Programme", "Year",
            "Location", "Module",
            "Availability", "Password"]
        fieldValues = [
            self.form["firstname"].get(),
            self.form["lastname"].get(),
            self.form["prog"].get(),
            self.form["year"].get(),
            self.form["loc"].get(),
            self.form["mod"].get(),
            ",".join(["".join([str(self.form["timeVars"][i][j].get())
                for j in range(3)]) for i in range(7)]),
            self.form["password"].get()
        ]
        fieldValues = multpasswordbox(msg, title, fieldNames, fieldValues)
        if fieldValues is None:
            sys.exit(0)
        # make sure that none of the fields were left blank
        while 1:
            errmsg = ""
            for i, name in enumerate(fieldNames):
                if fieldValues[i].strip() == "":
                    errmsg += "{} is a required field\n\n".format(name)
            if errmsg == "":
                break # no problems found
            fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
            if fieldValues is None:
                break
        if fieldValues is None:
            sys.exit(0)
        #print("Reply was:{}".format(fieldValues))

        self.firstname = fieldValues[0].strip()
        self.surname = fieldValues[1].strip()
        self.programme = fieldValues[2].strip()
        self.yearofstudy = fieldValues[3].strip()
        self.campuslocation = fieldValues[4].strip()
        self.modulename = fieldValues[5].strip()
        self.availability = fieldValues[6].strip()
        self.password = fieldValues[7]

        requests[requestid] = None # adds this request ID to the (unsaved) list of requests

    def display_All(self):
        print("Request ID = ", self.requestid, end=', ')
        print("Password = ", self.password)
        print(self.firstname+' '+self.surname,
            self.programme+' year '+self.yearofstudy,
            self.campuslocation, sep=', ')
        print("Module Name = ", self.modulename)
        print("Availability = ", self.availability)

    def display_Restricted(self):
        print(self.programme+' year '+self.yearofstudy,
            self.campuslocation, sep=', ')
        print("Module Name = ", self.modulename)
        print("Availability = ", self.availability)

# generate a random candidate (6 digit) request ID
# return it if it's not already in use
# otherwise, loop until a free ID is found
def generate_Random():
    global requests
    newId = 0 # use a distinguished, invalid value to start the loop
    while newId == 0 or newId in requests: # reject candidate ID if invalid or already exists
        newId = str(randrange(1e5,1e6)) # generate a candidate 6-digit number
    #print("+"+newId)
    return newId

def main():
    global root
    choiceSelection = choicebox(
        "Welcome to UWS Study Buddy App",
        "Press ENTER to make a new request",
        choices=["New Request"], preselect=0)
    if choiceSelection is None:
        sys.exit(0)
    root = Tk()
    newId = generate_Random()
    request = Request(newId)
    request.display_Restricted()

# run main() if this file is not being used otherwise, e.g. by test
if __name__ == "__main__":
    main()
