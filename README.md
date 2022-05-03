# Lpa Assignment Sheet Reader
This is a summer hobby project written in python, the purpose of this project is to read out lpa assignment sheets and put that data into a to do list
## Information
### Unpackaged:
To use this program in its non-executable form, the program needs to be launched from a console:
This command can be used: 

`python3 ./AssignmentSheetReader.py <file location>`

file location must be supplied with the full file path, including drive name, and file extension  
Example: `C:\Users\<user>\Doccuments\file.docx`  
Currently, the program only supports ".docx" or Microsoft Word Doccument files.

## Development Status:
- 5/3/2022: Program is not opperational yet
- 5/3/2022 (part 2): Program is not opperational yet, but now can verify that the requested file exists, and that it is a supported type

### Development Roadmap:
Tasks:  
- [x] Create function to verify that desired file exists, and is supported
- [ ] create function to access and open file
- [ ] Create Function to parse file and collect all assignments
- [ ] Create Function to add all assigments to a file of choice (.docx or .csv)
- [ ] Allow for windows "open with" menu to open a file using this program
- [ ] Create GUI for program (graphical user interface)
- [ ] Cemove functions that were neccesary when program was console based (after GUI is finished)
- [ ] Add support for more file types
