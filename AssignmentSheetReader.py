#this is a system that when supplied with a Logos prep assignment sheet, can read out assignment sheets and do multiple things with that data


#setting up packages
from importlib.util import LazyLoader
from msilib.schema import File
from operator import truediv
from pydoc import isdata
from tkinter.messagebox import OKCANCEL, askretrycancel
from turtle import bgcolor, color, left, right, width
from types import NoneType
from webbrowser import get
import docx
from docx import Document
import sys
from pathlib import Path
from dateutil.parser import parse
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import tkinter.font as TkFont
import glob
from PIL import Image, ImageTk


#setting up vars
global DocumentRef      #Defining as global var
global IsAssignmentRow      #Defining as global var
global Assignments      #Defining as global var
global TempAssignmentStr        #Defining as global var
global AssignmentsAndDueDates       #Defining as global var
global Dates        #Defining as global var
global LaunchArgument
global DocPath
global FileName
global FileType
global FileInfo
global Subject
global NoFileErrors
global SideBarTextHeight
global IsDevModeActive
global Width
global IsDarkModeActive
FileName = "" #String, Contains the name of the assignment sheet but not the file extension     -now unnessecary
FileType = "" #String, format will be in a standard file extension IE: "doc", will be grabbed when file is chosen by reading it from file name      !in use
SupportedFileTypes = ["docx", "doc"] #These are the only two types of files that assignment sheets will be made as
FileInput = "" #String, Contains both the file name and file extension      -now unnessecary
NoFileErrors = True     #This bool is related to CheckForFile() and CheckIfIsSupported()
DocumentRef = NoneType      #This is defined as empty, but will be the var containing the refrence to the document file
IsAssignmentRow = True      #This var is used to allow for removing everything that is not part of an assignment
Assignments = []        #This list will contain all assignment tasks
Dates = []      #This list will contain all due dates
TempAssignmentStr = ""      #This string is used to hold information from each cell untill it can be added into the list
AssignmentsAndDueDates = {      #This will be used to hold each assignment and its cooresponding due date
    "" : ""
}
SideBarTextHeight = 40
IsDevModeActive = False
Width = True
IsDarkModeActive = True
#collecting launch arg data
'''
LaunchArgument = str(sys.argv[1])       #FIX BEFORE RELEASE! this grabs the file path passed as a launch argument
LaunchArgumentSubject = str(sys.argv[2])      #FIX BEFORE RELEASE! this grabs the subject name passed as a launch argument  
print(LaunchArgument)   #output (remove in release)
print(LaunchArgumentSubject) #output (remove in release)
'''

#Parsing The provided File name and subject
LaunchArgument = str(sys.argv[1])
if LaunchArgument == "Dev-Mode":
    IsDevModeActive = True

#Checking that file type is supported, and that file exists
def CheckForFile():
    global NoFileErrors
    if DocPath.is_file() == False:      #this will be replaced with a popup (when this program is given a GUI)
        print("Error: " + FileName + " could not be found, please verify that the path is correct")
        NoFileErrors = False        #Since there are no errors, this allows the program to continue
        #exit()      #will not exit when program has GUI, will only allow to chose another path
        return NoFileErrors
def CheckIfIsSupported():
    if SupportedFileTypes.__contains__(FileType) == False:      #this will be replaced with a popup (when this program is given a GUI)
        print("Error: " + FileType + " files are not currently supported")
        NoFileErrors = False        #Since there are no errors, this allows the program to continue
        #exit()      #will not exit when program has GUI, will only allow to chose another path
        return NoFileErrors
#Accessing file
def OpenFile():
    if NoFileErrors == True:        #will only run if there are no file errors
        global DocumentRef      #allows for the function to access the var
        DocumentRef = docx.Document(DocPath)      #opens the doccument and creates a variable that refrences it
    else:
        print("Error: file error")      #seccond warning, though this function should not even be able to be run in the first place if there is a file error
        #exit()      #will not exit when program has GUI, will throw pop up
#Reading out file info and saving assignments and dates
def GetDocumentData():
    global DocumentRef      #Allows for function to access var
    global Assignments      #Allows for function to access var
    global AssignmentsAndDueDates       #Allows for function to access var
    global TempAssignmentStr        #Allows for function to access var
    global Dates        #Allows for function to access var
    for p in DocumentRef.tables:    #Runs through all tables in doccument
        for q in p.rows:        #runs through all rows in each table
            TempAssignmentStr = ""      #clears temp var
            IsAssignmentRow = False   
            for r in q.cells:   #reads thru each cell
                if "Assignments/ Instructions" in r.text:   #if the first cell says "Assignments/ Instructions" then add whole row to array
                    IsAssignmentRow = True
                if IsAssignmentRow == True:
                    #print(r.text)       #remove in release
                    if "/" in r.text and any(c.isalpha() for c in r.text) == False:     #Makes sure all dates get added to the date array
                        SplitDates = r.text.split("\n")
                        for s in SplitDates:
                            Dates.append(s)
                    else:       #Adds Tasks to assignment array
                        SplitAssignments = r.text.split("\n")
                        for t in SplitAssignments:
                            Assignments.append(t)
            
#Handles assignment and due date data 
def ParseDocumentData():        #Combines assignments list and due dates list into a dictionary
    global Assignments    #Allows for function to access var
    global Dates        #Allows for function to access var
    global AssignmentsAndDueDates       #Allows for function to access var
    for a in Dates:     #clears empty strings
        if a == '':     #This removes empty string
            Dates.remove(a)
        if a == "":     #this also removes empty Strings, not all get removed for some reason idk
            Dates.remove(a)
    for b in Assignments:       #clears empty strings, and ¨Assignments/ Instructions" 
        if b == "Assignments/ Instructions":
            Assignments.remove(b)
        if b == '':
            Assignments.remove(b)
    for i in Assignments:
        AssignmentsAndDueDates[i] = Dates[Assignments.index(i)]
def GetSubject():
    global Subject
    global SideBarTextHeight
    Subject = sd.askstring(title="Choose Subject", prompt="Please type the name of the subject this assignment sheet pertains to: ")
    RightSideBar.create_text(135, SideBarTextHeight, text=Subject, fill="#bb86fc", font=BodyFont)
    Subject = " (" + Subject + ") "
    SideBarTextHeight = SideBarTextHeight + 20

def FileDialog():
    global LaunchArgument
    global DocPath
    global FileName
    global FileType
    global FileInfo
    FileName = fd.askopenfilename(
        title='select an assignment sheet',
        initialdir='/'
    )
    DocPath = Path(FileName)    #initializes a path refrence to the given file
    FileInfo = FileName.split(".")   #creates an array containing the split string, the latter half of the split string is the file extension
    FileType = FileInfo[1]  #saving file extension
    print(FileType)
    GetSubject()
def RightSideMenuExpand():  #expands right menu bar
    global Width
    if Width == True:
        SideMenuPanel.config(width=200)
        SideBarMenuButton.place(x=-75, y=0, relwidth="1", relheight=".1")
        SideBarFileButton.config(text="Open File")
        SideBarFileButton.place(x=-50, y=45, relwidth="1", relheight=".1")
        SideBarDarkModeButton.config(text="Dark Mode")
        SideBarDarkModeButton.place(x=-45, y=90, relwidth="1", relheight=".1")
        SideBarSettingsButton.config(text="Settings")
        SideBarSettingsButton.place(x=-55, y=480, relwidth="1", relheight=".1")
    else:
        SideMenuPanel.config(width=50)
        SideBarMenuButton.place(x=0, y=0, relwidth="1", relheight=".1")
        SideBarFileButton.config(text="FM")
        SideBarFileButton.place(x=0, y=45, relwidth="1", relheight=".1")
        SideBarDarkModeButton.config(text="DM")
        SideBarDarkModeButton.place(x=0, y=90, relwidth="1", relheight=".1")
        SideBarSettingsButton.config(text="SM")
        SideBarSettingsButton.place(x=0, y=480, relwidth="1", relheight=".1")
    Width = not Width
def PlaceholderFunction():
    print("button")
def ToggleDarkMode():   #toggles dark mode
    global IsDarkModeActive
    if IsDarkModeActive == True:
        print(IsDarkModeActive)
        Window.configure(bg="#ffffff")
        RightSideBar.configure(bg="#6200ee")
        RightSideBar.itemconfig(RightSideBarText, fill='White')
        SideMenuPanel.config(bg="#6200ee")
        SideBarMenuButton.config(bg="#6200ee")
        SideBarFileButton.config(bg="#6200ee", fg="white")
        SideBarDarkModeButton.config(bg="#6200ee", fg="white")
        SideBarSettingsButton.config(bg="#6200ee", fg="white")
    else:
        Window.configure(bg="#121212")
        RightSideBar.configure(bg="#1F1B24")
        RightSideBar.itemconfig(RightSideBarText, fill='#bb86fc')
        SideMenuPanel.config(bg="#1f1f1f")
        SideBarMenuButton.config(bg="#1f1f1f")
        SideBarFileButton.config(bg="#1f1f1f", fg="#bb86fc")
        SideBarDarkModeButton.config(bg="#1f1f1f", fg="#bb86fc")
        SideBarSettingsButton.config(bg="#1f1f1f", fg="#bb86fc")

    IsDarkModeActive = not IsDarkModeActive
    

#setting up GUI
Window = tk.Tk()    #setup window
HeaderFont = TkFont.Font(family="SF Pro Display", size=16, weight="bold")     #Initialize Font standard for headers
BodyFont = TkFont.Font(family="San Fransisco", size=14, weight="normal")    #initialize font standard for body text
Window.title("Lpa assignment sheet tool")   #set window title
Window.geometry('960x540+50+50')    #set window default size
Window.configure(bg="#121212")  #set background color(default dark mode)
Window.resizable(False, False)
MenuIcon = Image.open("Assets/Menu.png")
MenuPic = ImageTk.PhotoImage(MenuIcon, color)
menubar = Menu(Window)  #setup menu bar
Window.config(menu=menubar)     #Add menu bar to window
fileMenu = Menu(menubar)       #add "File" menu to menu bar
fileMenu.add_command(label="Open File", command=FileDialog)     #add "Open File" button to file menu
fileMenu.add_command(label="Exit")      #Add "exit" button to file menu
menubar.add_cascade(label="File", menu=fileMenu)    #set up file menu
RightSideBar=tk.Canvas(Window, background="#1F1B24", height=960, width=270, bd="0", highlightthickness="0")     #create right side bar
RightSideBar.pack(side=RIGHT)       #add right side bar to the window
RightSideBarText=RightSideBar.create_text(135, 20, text="Added Subjects:", fill="#bb86fc", font=HeaderFont)     #add right side bar header
SideMenuPanel=tk.Canvas(Window, background="#1f1f1f", height=900, width=50, bd="0", highlightthickness="0")     #Create left side bar
SideMenuPanel.pack(side=LEFT)   #add left side bar
SideBarMenuButton=tk.Button(SideMenuPanel, image=MenuPic, command=RightSideMenuExpand, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialize Button
SideBarMenuButton.place(x=0, y=0, relwidth="1", relheight=".1") #Place Menu button
SideBarFileButton = tk.Button(SideMenuPanel, text="FM", font=BodyFont, command=FileDialog, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialize Button
SideBarFileButton.place(x=0, y=45, relwidth="1", relheight=".1")    #Add open file button
SideBarDarkModeButton = tk.Button(SideMenuPanel, text="DM", font=BodyFont, command=ToggleDarkMode, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialze button
SideBarDarkModeButton.place(x=0, y=90, relwidth="1", relheight=".1")    #Add toggle dark mode button
SideBarSettingsButton = tk.Button(SideMenuPanel, text="SM", font=BodyFont, command=PlaceholderFunction, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialize Button
SideBarSettingsButton.place(x=0, y=480, relwidth="1", relheight=".1")   #Place Settings Button

#Dev Menu Setup
if IsDevModeActive == True:
    DevMenu = Menu(menubar)
    DevMenu.add_command(label="Add Subject", command=GetSubject)
    DevMenu.add_command(label="Unused")
    DevMenu.add_command(label="Unused")
    DevMenu.add_command(label="Unused")
    menubar.add_cascade(label="Dev Tools", menu=DevMenu)



Window.mainloop()


for c in AssignmentsAndDueDates:        #Remove in release, this prints out data from the dictionary 
    print(c + Subject + "     " + AssignmentsAndDueDates[c])
    print("\n")