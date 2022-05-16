# Lpa Assignment Sheet Reader
This is a summer hobby project written in python, the purpose of this project is to read out lpa assignment sheets and put that data into a to do list

## Development Status:
- 5/3/2022: Program is not opperational yet
- 5/3/2022 (part 2): Program is not opperational yet, but now can verify that the requested file exists, and that it is a supported type
- 5/5/2022: Program now can open the requested file, and read it, then detects when a row contains the string "Assignments/ Instructions", and then prints the entire rows information out to the console, cleaned up previous work (2 hours work)
- 5/5/2022 (part 2): Now removes empty strings, and combines the list of assignments and list of due dates into a dictionary (1 hours work)
- 5/8/2022: Now has a GUI, can open file and select Subject, does not add data to a list yet (2 hours work)
- 5/8/2022 (part 2): Added constant stylizing, side bar is now functional, added dev menu, only accessable by using "Dev-Mode" as a launch argument (3 hours work)
- 5/9/2022: Improved UI, added settings window (empty) (1.2 hours work)
- 5/15/2022: Added settings save file, file preview panel (2 hours work)

### Development Roadmap:
Tasks:  
- [x] Create function to verify that desired file exists, and is supported [**Finished 5/3/2022**]
- [x] Create function to access and open requested file [**Finished 5/5/2022**]
- [x] Create Function to parse file and collect all assignments [**Finished 5/5/2022**]
- [ ] Add Settings Menu [**Began 5/9/2022**]
- [ ] Create Error Handing, when there are not enough due dates, allow for the assignments to share due dates
- [ ] Create Function to add all assigments to a file of choice (.docx or .csv)
- [ ] Allow for windows "open with" menu to open a file using this program
- [ ] Create GUI for program (graphical user interface) [**Began 5/8/2022**]
- [ ] Create Icons for GUI (background color: #1F1B24, icon color: #bb86fc)
- [x] Remove functions that were neccesary when program was console based (after GUI is finished)
- [ ] Add support for more file types  

## Other
Have an idea for a feature? Create an issue with your suggestion, and it might get added! ;)

## Dev notes
### Functions:
 - CheckForFile() - this function verifies that the given file path exists
 - CheckIfIsSupported() - this function verifies that the file type is supported
 - OpenFile() - This function only runs if there are no file errors, this prepares the file to be read out
 - GetDocumentData() - Reads out file data and sorts it into the correct arrays
 - ParseDocumentData() - Removes unwanted data and combines Assignments and Dates into a dictionary
 - GetSubject() - Pop up dialog to assign a subject to each task
 - FileDialog() - Pop up file selection dialog (also parses file path)

### Pre-Release surveys:
 - [x] Take survey on what computers people use [Data: Mac: 50%, Chromebook: 5%, Windows: 45%]
 - [x] Light Mode/Dark Mode Survey (Results: Dark mode/Allow for user to decide) [Data: Dark: 61%, Light:13%, choose: 26%]
 - [ ] Take survey on how much people are willing to pay for the tool
 - [ ] How people want the to-do list exported (options: Spreadsheet, Document)
 - [ ] Do people use their school laptops for homework
### Survey desicions 
 - Package software for: Mac, windows
 - Apperance mode: both, let user decide
