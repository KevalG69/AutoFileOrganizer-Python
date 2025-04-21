import os
import shutil
import time

#external library
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



#source folder
SOURCE_FOLDER = "D:\downloaded"

#making dictionary of destination folder path to move file with particular extensions

dest_folders = {
    "pdf" :"D:\downloaded\Project\AutoFileOrganizer\Organized\PDFs",

    "png" :"D:\downloaded\Project\AutoFileOrganizer\Organized\Images",
    "jpg" :"D:\downloaded\Project\AutoFileOrganizer\Organized\Images",
    "jpeg" :"D:\downloaded\Project\AutoFileOrganizer\Organized\Images",
    "txt" :"D:\downloaded\Project\AutoFileOrganizer\Organized\TextFiles",
    "tmp" :"D:\downloaded\Project\AutoFileOrganizer\Organized\Trash"
    
}


#creating folder if not existed
for folder in dest_folders.values():
    os.makedirs(folder,exist_ok=True)


#organize file
def organize_file():

    #iterating through file in directory   
    '''--> 1.iterate to all file available in D:\donwloaded or SOURCE_FOLDER '''
    for fileName in os.listdir(SOURCE_FOLDER):

        '''
        --> 2.Get proper file path like D:\donwloaded\test.txt to do operations

            os.path.join() is used to make file path using "\" according to operating
            systeme so don't have to create manually like this
                SOURCE_FOLDER + "\" + fileName
            
            it will automatically add \ or /
            like if SOURCE_FOLDER = "D:\downloaded"
            fileName = test.text 
            the file_path will get D:\donwloaded\test.text
        '''
        file_path = os.path.join(SOURCE_FOLDER,fileName)

        '''
        --> 3.not check the file which get from path is file or not

            os.path.isfile used to check "file_path" have file or not        
        '''
        if os.path.isfile(file_path):
            #if file found/isfile then now get the extension of file like
            #it from file name text.txt -> text . txt -> [-1] ->txt
            extension = fileName.split(".")[-1].lower()

    
       #--> 4. get destination folder path to move file
        
            #now get the destinatio folder according to extenstion
            # get(txt)-> dest_folders['txt] -> D:\downloaded\Project\AutoFileOrganizer\Organized\TextFiles
            dest_folder = dest_folders.get(extension)

        #-->5. now if proper destination folder path found move the file there

            if dest_folder:
                
                #exception handle to handle run time error
                try:
                    '''
        -->6. now move file from file_path which will get file to dest folder by using 
                shutil library move function which useded 
                    '''
                    shutil.move(file_path, os.path.join(dest_folder,fileName))
                    print(f"Moved {fileName} to {dest_folder}")

                except Exception as error:
                    
                    print(f"Failed to move {fileName} : {error}")


#now check if file added to directory
class FileOrganizerHandler(FileSystemEventHandler):
    
    '''1. run when object of this file is created'''
    def on_created(self, event):
    
        #check if change happened related to file not folder
        if not event.is_directory:
            #if change related to file then run this
            organize_file()


#watch file change in folder
def watch_folder(path):

    #create object of Fi
    event_handler = FileOrganizerHandler()

    observer = Observer()

    '''
       1.observer is used to watch file changes in directory
       2.schedule if observer's function in which arugment pass which tell that
        "Hey, watch this folder and use this handler to respond to any changes."
       3.path used to tell which directory to watch for changes
       4.recursive=False: Means "Only watch this folder, not its subfolders."
    '''
    observer.schedule(event_handler,path,recursive=False)
    observer.start()

    try:
        '''
        this infinite loop which keep script alive so it keep running
        '''
        while True:
            time.sleep(10)

    #stop the script if Ctrl + C pressed which will raise KeyboardInterrupt exception
    except KeyboardInterrupt:
        observer.stop()

    '''
    This tells Python:
        "Wait here until the observer has fully stopped before exiting the program."
    '''
    observer.join()


'''
This is Python’s way of saying:
"Only run this part if the script is being run directly, not if it's being imported as a module into another script."
'''

if __name__ == "__main__":
    watch_folder(SOURCE_FOLDER)