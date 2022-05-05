#this is a system that when supplied with a Logos prep assignment sheet, can read out assignment sheets and do multiple things with that data

#setting up packages
from asyncio.windows_events import NULL
from types import NoneType
import docx
from docx import Document
import sys
from pathlib import Path


#setting up vars
FileName = "" #String, Contains the name of the assignment sheet but not the file extension     -now unnessecary
FileType = "" #String, format will be in a standard file extension IE: "doc", will be grabbed when file is chosen by reading it from file name      !in use
SupportedFileTypes = ["docx", "doc"] #These are the only two types of files that assignment sheets will be made as
FileInput = "" #String, Contains both the file name and file extension      -now unnessecary
NoFileErrors = True
global DocumentRef
DocumentRef = NoneType

#collecting launch arg data
LaunchArgument = str(sys.argv[1])
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
        NoFileErrors = False
        exit()      #will not exit when program has GUI, will only allow to chose another path
def CheckIfIsSupported():
    if SupportedFileTypes.__contains__(FileType) == False:      #this will be replaced with a popup (when this program is given a GUI)
        print("Error: " + FileType + " files are not currently supported")
        NoFileErrors = False
        exit()      #will not exit when program has GUI, will only allow to chose another path

CheckForFile()
CheckIfIsSupported()

#Accessing file
def OpenFile():
    if NoFileErrors == True:        #will only run if there are no file errors
        global DocumentRef
        DocumentRef = docx.Document(DocPath)      #opens the doccument and creates a variable that refrences it
    else:
        print("Error: file error")      #seccond warning, though this function should not even be able to be run in the first place if there is a file error
        exit()      #will not exit when program has GUI, will throw pop up

OpenFile()

#Reading out file info
def GetDoccumentData():
    global DocumentRef
    for p in DocumentRef.tables:
        for q in p.rows:
            for r in q.cells:
                for s in r.paragraphs:
                    print(s.text)

GetDoccumentData()



    

#DOCX file setup