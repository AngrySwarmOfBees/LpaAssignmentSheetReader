#this is a system that when supplied with a Logos prep assignment sheet, can read out assignment sheets and do multiple things with that data

#setting up packages
from ast import Assign
from asyncio.windows_events import NULL
from operator import truediv
from types import NoneType
import docx
from docx import Document
import sys
from pathlib import Path
from dateutil.parser import parse   


#setting up vars
FileName = "" #String, Contains the name of the assignment sheet but not the file extension     -now unnessecary
FileType = "" #String, format will be in a standard file extension IE: "doc", will be grabbed when file is chosen by reading it from file name      !in use
SupportedFileTypes = ["docx", "doc"] #These are the only two types of files that assignment sheets will be made as
FileInput = "" #String, Contains both the file name and file extension      -now unnessecary
NoFileErrors = True     #This bool is related to CheckForFile() and CheckIfIsSupported()
global DocumentRef      #Defining as global var
global IsAssignmentRow      #Defining as global var
global Assignments      #Defining as global var
global TempAssignmentStr        #Defining as global var
global AssignmentsAndDueDates       #Defining as global var
global Dates        #Defining as global var
DocumentRef = NoneType      #This is defined as empty, but will be the var containing the refrence to the document file
IsAssignmentRow = True      #This var is used to allow for removing everything that is not part of an assignment
Assignments = []        #This list will contain all assignment tasks
Dates = []      #This list will contain all due dates
TempAssignmentStr = ""      #This string is used to hold information from each cell untill it can be added into the list
AssignmentsAndDueDates = {      #This will be used to hold each assignment and its cooresponding due date
    "" : ""
}

#collecting launch arg data
LaunchArgument = str(sys.argv[1])       #FIX BEFORE RELEASE! this grabs the file path passed as a launch argument
print(LaunchArgument)   #output (remove in release)

#Parsing The provided File name
DocPath = Path(LaunchArgument)      #initializes a path refrence to the given file
FileInfo = LaunchArgument.split(".")        #creates an array containing the split string, the latter half of the split string is the file extension
FileType = FileInfo[1]  #saving file extension
print(FileType)     #output(remove in release)

#Checking that file type is supported, and that file exists
def CheckForFile():
    if DocPath.is_file() == False:      #this will be replaced with a popup (when this program is given a GUI)
        print("Error: " + LaunchArgument + " could not be found, please verify that the path is correct")
        NoFileErrors = False        #Since there are no errors, this allows the program to continue
        exit()      #will not exit when program has GUI, will only allow to chose another path
def CheckIfIsSupported():
    if SupportedFileTypes.__contains__(FileType) == False:      #this will be replaced with a popup (when this program is given a GUI)
        print("Error: " + FileType + " files are not currently supported")
        NoFileErrors = False        #Since there are no errors, this allows the program to continue
        exit()      #will not exit when program has GUI, will only allow to chose another path

CheckForFile()
CheckIfIsSupported()

#Accessing file
def OpenFile():
    if NoFileErrors == True:        #will only run if there are no file errors
        global DocumentRef      #allows for the function to access the var
        DocumentRef = docx.Document(DocPath)      #opens the doccument and creates a variable that refrences it
    else:
        print("Error: file error")      #seccond warning, though this function should not even be able to be run in the first place if there is a file error
        exit()      #will not exit when program has GUI, will throw pop up

OpenFile()

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
        if a == '':
            Dates.remove(a)
        if a == "":
            Dates.remove(a)
    for b in Assignments:       #clears empty strings
        if b == "Assignments/ Instructions":
            Assignments.remove(b)
        if b == '':
            Assignments.remove(b)
    for i in Assignments:
        AssignmentsAndDueDates[i] = Dates[Assignments.index(i)]

GetDocumentData()
ParseDocumentData()

for c in AssignmentsAndDueDates:
    print(c + "     " + AssignmentsAndDueDates[c])
    print("\n")