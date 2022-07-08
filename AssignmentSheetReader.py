#this is a system that when supplied with a Logos prep assignment sheet, can read out assignment sheets and do multiple things with that data


#setting up packages
from ast import Assign
from importlib.util import LazyLoader
from msilib.schema import File
from operator import truediv
from pydoc import isdata
from textwrap import fill
from tkinter.messagebox import OKCANCEL, askretrycancel
from turtle import bgcolor, color, left, right, width
from types import NoneType
from webbrowser import get
from xml.etree.ElementTree import tostring
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
import json
import csv
from datetime import date


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
global RightSideBarBodyText
global ExportFileType
global SettingsDict
global SubjectList
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
AssignmentsAndDueDates = {}  #This will be used to hold each assignment and its cooresponding due date
SideBarTextHeight = 40
IsDevModeActive = False
Width = True
IsDarkModeActive = True
RightSideBarBodyText = []
ExportFileType = "csv"
SettingsDict = {
    
}
SubjectList = []
#collecting launch arg data
'''
LaunchArgument = str(sys.argv[1])       #FIX BEFORE RELEASE! this grabs the file path passed as a launch argument
LaunchArgumentSubject = str(sys.argv[2])      #FIX BEFORE RELEASE! this grabs the subject name passed as a launch argument  
print(LaunchArgument)   #output (remove in release)
print(LaunchArgumentSubject) #output (remove in release)
'''

#Parsing The provided File name and subject

if sys.argv.__contains__('Dev-Mode') == True:
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
        if b.__contains__("Assignmnets/ Instructions") == True:
            Assignments.remove(b)
        if b.__contains__('Assignmnets/ Instructions') == True:
            Assignments.remove(b)
        if b == '':
            Assignments.remove(b)
    for i in Assignments:
        AssignmentsAndDueDates[i] = Dates[Assignments.index(i)]
        tempstr = str(i + "   " + Dates[Assignments.index(i)] + "\n" + "\n")
        DocumentCanvas.insert(DocumentText, tk.END, tempstr)
        DocumentCanvas.config(scrollregion=DocumentCanvas.bbox('all'))

#Reading out file info and saving assignments and dates 
def GetDocumentData():
    global DocumentRef      #Allows for function to access var
    global Assignments      #Allows for function to access var
    global AssignmentsAndDueDates       #Allows for function to access var
    global TempAssignmentStr        #Allows for function to access var
    global Dates        #Allows for function to access var
    global Subject
    global SubjectList
    Assignments.clear()
    Dates.clear()
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
                            if t.__contains__("Assignments/ Instructions") == False:
                                Assignments.append(t)
                                SubjectList.append(Subject)
    ParseDocumentData()
    
def GetSubject():
    global Subject
    global SideBarTextHeight
    global RightSideBarBodyText
    Subject = sd.askstring(title="Choose Subject", prompt="Please type the name of the subject this assignment sheet pertains to: ")
    Temp = RightSideBar.create_text(135, SideBarTextHeight, text=Subject, fill="#bb86fc", font=BodyFont)
    RightSideBarBodyText.append(Temp)
    tempstr = "\n" + Subject + ": \n" + "\n"
    DocumentCanvas.insert(DocumentText, tk.END, tempstr)
    SideBarTextHeight = SideBarTextHeight + 20
    GetDocumentData()

def OpenFile():
    CheckForFile()
    CheckIfIsSupported()
    if NoFileErrors == True:        #will only run if there are no file errors
        global DocumentRef      #allows for the function to access the var
        DocumentRef = docx.Document(DocPath)      #opens the doccument and creates a variable that refrences it
    else:
        print("Error: file error")      #seccond warning, though this function should not even be able to be run in the first place if there is a file error
        #exit()      #will not exit when program has GUI, will throw pop up
    GetSubject()

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
    OpenFile()

def LoadSavedSettings():
    global SettingsDict
    global ExportFileType
    global IsDarkModeActive
    with open('Settings.json', 'r') as S:
        SettingsDict = json.load(S)
    ExportFileType.set(value=SettingsDict["List File Type"])
    IsDarkModeActive = value=SettingsDict["Dark Mode"]
    IsDarkModeActive = not IsDarkModeActive
    ToggleDarkMode()

def UpdateSavedSettings():  #This saves new settings to a json file
    global SettingsDict
    global ExportFileType
    global IsDarkModeActive
    print("Updated Settings File")
    SettingsDict["List File Type"] = ExportFileType.get()   #Adding setting to dictionary
    SettingsDict["Dark Mode"] = IsDarkModeActive    #Adding setting to dictionary
    with open('Settings.json', 'w') as S:   #opens Settings.json
        json.dump(SettingsDict, S)  #saves dictionary to json file
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
        DocumentCanvas.itemconfig(DocumentText, fill="#6200ee")
        DocumentScrollBar.config(bg="white")
        for i in RightSideBarBodyText:
            RightSideBar.itemconfig(i, fill='White')
    else:
        Window.configure(bg="#121212")
        RightSideBar.configure(bg="#1F1B24")
        RightSideBar.itemconfig(RightSideBarText, fill='#bb86fc')
        SideMenuPanel.config(bg="#1f1f1f")
        SideBarMenuButton.config(bg="#1f1f1f")
        SideBarFileButton.config(bg="#1f1f1f", fg="#bb86fc")
        SideBarDarkModeButton.config(bg="#1f1f1f", fg="#bb86fc")
        SideBarSettingsButton.config(bg="#1f1f1f", fg="#bb86fc")
        DocumentCanvas.itemconfig(DocumentText, fill="#bb86fc")
        DocumentScrollBar.config(bg="#bb86fc")
        for i in RightSideBarBodyText:
            RightSideBar.itemconfig(i, fill='#bb86fc')

    IsDarkModeActive = not IsDarkModeActive
    UpdateSavedSettings()

def OpenSettingsWindow():       #Settings window setup
    global IsDarkModeActive
    global ExportFileType
    SettingsWindow = tk.Tk()
    SettingsWindow.title("Settings")
    SettingsWindow.geometry('450x540')
    SettingsCanvas=tk.Canvas(SettingsWindow, width=450, height=540, borderwidth=0, highlightthickness=0)
    SettingsCanvas.pack(side=TOP)
    ExportFileType = tk.StringVar(SettingsCanvas)
    SettingsHeader = SettingsCanvas.create_text(50, 25, text="Settings:", font=HeaderFont)
    FileSaveTypeText = SettingsCanvas.create_text(75, 65, text="Export as:", font=BodyFont)
    FileSaveTypeButtonDoc = tk.Radiobutton(SettingsCanvas, text="docx", font=BodyFont, value="docx", variable=ExportFileType, command=UpdateSavedSettings)
    FileSaveTypeButtonDoc.place(x=150, y= 50)
    FileSaveTypeButtonCsv = tk.Radiobutton(SettingsCanvas, text="csv", font=BodyFont, value="csv", variable=ExportFileType, command=UpdateSavedSettings)
    FileSaveTypeButtonCsv.place(x=300, y= 50)
    FileSaveTypeButtonCsv.select()
    Option2Text = SettingsCanvas.create_text(65, 105, text="Option2", font=BodyFont)
    Option2Button = tk.Checkbutton(SettingsCanvas, text="Test", font=BodyFont)
    Option2Button.place(x=150, y= 90)
    DonateText = tk.Label(SettingsCanvas, text="Support this project and get early access to features", font=("San Fransisco", 12))
    DonateText.place(x=10, y=475)
    DonateButton = tk.Button(SettingsCanvas, command=PlaceholderFunction, width=7, anchor=tk.CENTER, text="Donate")
    DonateButton.place(x=375, y=475)
    if IsDarkModeActive == True:
        SettingsWindow.configure(bg="#121212")
        SettingsCanvas.configure(bg="#121212")
        SettingsCanvas.itemconfig(SettingsHeader, fill="#bb86fc")
        SettingsCanvas.itemconfig(FileSaveTypeText, fill="#bb86fc")
        SettingsCanvas.itemconfig(Option2Text, fill="#bb86fc")
        FileSaveTypeButtonDoc.configure(fg="#bb86fc", bg="#121212", activeforeground="#bb86fc", activebackground="#121212")
        FileSaveTypeButtonCsv.configure(fg="#bb86fc", bg="#121212", activeforeground="#bb86fc", activebackground="#121212")
        DonateText.configure(fg="#bb86fc", bg="#121212", activeforeground="#bb86fc", activebackground="#121212")
        DonateButton.configure(fg="#bb86fc", bg="#121212", activeforeground="#bb86fc", activebackground="#121212")
        Option2Button.configure(fg="#bb86fc", bg="#121212")
    else:
        SettingsWindow.configure(bg="White")
        SettingsCanvas.configure(bg="White")
        SettingsCanvas.itemconfig(SettingsHeader, fill="#6200ee")
        SettingsCanvas.itemconfig(FileSaveTypeText, fill="#6200ee")
        SettingsCanvas.itemconfig(Option2Text, fill="#6200ee")
        FileSaveTypeButtonDoc.configure(fg="#6200ee", bg="White", activeforeground="#6200ee", activebackground="White")
        FileSaveTypeButtonCsv.configure(fg="#6200ee", bg="White", activeforeground="#6200ee", activebackground="White")
        DonateText.configure(fg="#6200ee", bg="White", activeforeground="#6200ee", activebackground="White")
        DonateButton.configure(fg="#6200ee", bg="White", activeforeground="#6200ee", activebackground="White")
        Option2Button.configure(fg="#6200ee", bg="White")
    
#TO-Do list export function
def ExportToDoList():
    global AssignmentsAndDueDates
    global ExportFileType
    global SubjectList
    index = 0
    print(AssignmentsAndDueDates)
    print("Exporting")
    tempfieldnames = ['Task', 'Due Date', 'Subject', 'Completed']
    if ExportFileType.get() == "csv":   #csv file exporting
        today = date.today()
        exportfilenametemp = str(today) + ".csv"
        with open(exportfilenametemp, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=tempfieldnames)
            writer.writeheader()
            for key in AssignmentsAndDueDates.keys():
                csvfile.write("%s, %s, %s, %s\n" % (key, AssignmentsAndDueDates[key], SubjectList[index], "no"))
                index = index + 1
    else:
        today = date.today()
        exportfilenametemp = str(today) + ".docx"
    

    
    


#setting up GUI
Window = tk.Tk()    #setup window
ExportFileType = StringVar()
HeaderFont = TkFont.Font(family="SF Pro Display", size=16, weight="bold")     #Initialize Font standard for headers
BodyFont = TkFont.Font(family="San Fransisco", size=14, weight="normal")    #initialize font standard for body text
SubBodyFont = TkFont.Font(family="San Fransisco", size=5, weight="normal")
DarkModeStyle = ttk.Style()
DarkModeStyle.configure("Dark.Mode", foreground='#bb86fc')
LightModeStyle = ttk.Style()
LightModeStyle.configure("Light.Mode", foreground='#6200ee')
Window.title("Lpa assignment sheet tool")   #set window title   
Window.geometry('960x540+50+50')    #set window default size
Window.configure(bg="#121212")  #set background color(default dark mode)
Window.resizable(False, False)
MenuIcon = Image.open("Assets/Menu.png")
MenuIcon = MenuIcon.resize((48, 48))
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
ExportFileButton=tk.Button(RightSideBar, fg="#bb86fc", bg="#121212", activeforeground="#bb86fc", activebackground="#121212", command=ExportToDoList, text="Export List")
ExportFileButton.place(x=40, y=450, relheight=".1", relwidth=".7")
SideMenuPanel=tk.Canvas(Window, background="#1f1f1f", height=900, width=50, bd="0", highlightthickness="0")     #Create left side bar
SideMenuPanel.pack(side=LEFT)   #add left side bar
SideBarMenuButton=tk.Button(SideMenuPanel, image=MenuPic, command=RightSideMenuExpand, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialize Button
SideBarMenuButton.place(x=0, y=0, relwidth="1", relheight=".1") #Place Menu button
SideBarFileButton = tk.Button(SideMenuPanel, text="FM", font=BodyFont, command=FileDialog, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialize Button
SideBarFileButton.place(x=0, y=45, relwidth="1", relheight=".1")    #Add open file button
SideBarDarkModeButton = tk.Button(SideMenuPanel, text="DM", font=BodyFont, command=ToggleDarkMode, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialze button
SideBarDarkModeButton.place(x=0, y=90, relwidth="1", relheight=".1")    #Add toggle dark mode button
SideBarSettingsButton = tk.Button(SideMenuPanel, text="SM", font=BodyFont, command=OpenSettingsWindow, bg="#1f1f1f", fg="#bb86fc", activebackground="#363636", activeforeground="#bb86fc", bd="0")  #Initialize Button
SideBarSettingsButton.place(x=0, y=480, relwidth="1", relheight=".1")   #Place Settings Button
DocumentCanvas=tk.Canvas(Window, background="#1F1B24", width=612, height=9999, bd=0, highlightthickness="0")
DocumentCanvas.place(x=125, y=0, relwidth=".5", relheight="1")
DocumentText = DocumentCanvas.create_text(235, 25, font=BodyFont, text="Detected Tasks: \n", justify=tk.CENTER, width=450, anchor=tk.N, fill="#bb86fc")
DocumentScrollBar = tk.Scrollbar(DocumentCanvas, bg="#bb86fc", troughcolor="#bb86fc", activebackground="#1f1f1f", command=DocumentCanvas.yview)
DocumentScrollBar.pack(side=RIGHT, fill=Y)
DocumentCanvas.config(yscrollcommand=DocumentScrollBar.set)
LoadSavedSettings()

#Dev Menu Setup
if IsDevModeActive == True:
    DevMenu = Menu(menubar)
    DevMenu.add_command(label="Add Subject", command=GetSubject)
    DevMenu.add_command(label="Unused")
    DevMenu.add_command(label="Unused")
    DevMenu.add_command(label="Unused")
    menubar.add_cascade(label="Dev Tools", menu=DevMenu)
    

Window.mainloop()

'''
for c in AssignmentsAndDueDates:        #Remove in release, this prints out data from the dictionary 
    print(c + Subject + "     " + AssignmentsAndDueDates[c])
    print("\n")
'''