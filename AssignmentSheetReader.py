#this is a system that when supplied with a Logos prep assignment sheet, can read out assignment sheets and do multiple things with that data

#setting up packages
import docx
from docx import Document
import sys

#setting up vars
FileName = "" #String, Contains the name of the assignment sheet but not the file extension
FileType = "" #String, format will be in a standard file extension IE: "doc", will be grabbed when file is chosen by reading it from file name
SupportedFileTypes = ["docx", "doc"] #These are the only two types of files that assignment sheets will be made as
FileInput = "" #String, Contains both the file name and file extension

LaunchArgument = str(sys.argv[1])
print(LaunchArgument)

#Parsing The provided File name
FileInfo = LaunchArgument.split(".")
FileName = FileInfo[0]
FileType = FileInfo[1]
print(FileName)
print(FileType)

#DOCX file setup

