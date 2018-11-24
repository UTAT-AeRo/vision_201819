GUI to Identify 3-most damaged panels
---
# Description
Currently this script takes the images of damaged panels and copies them over to a new directory. The user can then check the images in the new directory and determine which are the top 3 most damaged, either manually, or by using a GUI (which will be developed later). The filenames of the damaged panels are taken from an input JSON file.

# Prerequisites
- Python 3

# Usage
When calling the script in the command prompt, the command line arguments are the path of the input JSON file, and the path of the desired output directory: `python script.py input.json output_directory`
Please note that depending on your OS, using backslashes or escape backslashes for the paths (and in the JSON file as well) will not work. The script works fine when you use forward slashes.

Actual sample usage:
`python C:/Users/Matthew/UTAT/GUI_Task/damaged_panels_imagefiltering.py C:/Users/Matthew/UTAT/GUI_Task/input.json C:/Users/Matthew/UTAT/damaged_panel_images`
