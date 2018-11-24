#GUI to Identify 3-most damaged panels
##############################################################################
#Currently this script takes the images of damaged panels and copies them
#over to a new directory. The user can then check the images in the new
#directory and determine which are the top 3 most damaged, either manually,
#or by using a GUI (which will be developed later).

import json
import os
import shutil
import sys

def main():
    
    command_line_args = sys.argv
    print("JSON filename is " + command_line_args[1])
    print("Output directory is " + command_line_args[2] + "\n")
    if len(command_line_args) != 3:
        print("ERROR: Path incorrect")
        return False #end program
    
    #path of the json file
    filename = command_line_args[1]
    #path of the new folder that stores the damaged images
    new_dir = command_line_args[2]
    #list to store filenames of damaged images
    damaged_filenames = []
    #whether or not the directory should be removed (if it already exists)
    remove = False

    try:
        with open(filename) as json_file: #open file
            data = json.load(json_file) #extracting data in json format
            for p in data["damaged"]:
                damaged_filenames += [p["filename"]]    
    except:
        print("ERROR: Could not open JSON file")
        return False #end program
    
    #check if there are actually files to move
    if len(damaged_filenames) == 0:
        print("ERROR: No image files to move")
        return False #end program
    
    if os.path.exists(new_dir): #if directory already exists
        print("ERROR: %s already exists\nDo you want to override? y/n" % new_dir)
        while True:
            response = input()
            if response == "n" or response == "N":
                print("%s was not created" % new_dir)
                return False #end program
            elif response == "y" or response == "Y":
                remove = True #directory already exists, go remove it
                break
            else:
                print("ERROR: Invalid Input. Enter y/n")
    
    #creating the new directory
    try:
        if remove == True:
            shutil.rmtree(new_dir) #remove the existing directory 
        os.mkdir(new_dir)
    except OSError:
        print("ERROR: OS Error")
        return False
    else:  
        print("%s was successfully created" % new_dir)
    
    #copy the image files to the new directory
    for i in range(0,len(damaged_filenames),1):
        #check if image file path is legitimate
        if os.path.isfile(damaged_filenames[i]) == True:
            shutil.copy(damaged_filenames[i],new_dir)
        else:
            print("ERROR: Could not copy %s\nOperation Aborted" % damaged_filenames[i])
            return False #end program

    return True #finish program
    
main()
