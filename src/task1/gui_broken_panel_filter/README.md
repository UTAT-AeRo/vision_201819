GUI Broken Panel Filter
---
# Description
	This is the "tinder" app for broken solar panels. It displays one image at a time, and the user either `"swipes right"` on the `truly damaged` solar panel photos. Likewise, you `"swipe left"` on undamaged solar panels. If the user makes a mistake, they can press the up arrow key to `go back`.

# Prerequisites
	The script requires `tkinter`, `sys`, `json`, and from `PIL` it imports `ImageTk`, `Image`. And `Python3`.
	Note that no imports are necessary as all of these requirements are included in python3

# Usage
	Use: `python3 gui_sorter_working_prototype.py --from json_name.json --to out_json_name.json`
	* json_name.json is the file that contains the names of the images in the format
	stated on the trello board
	* out_json_name.json is the name of the json file to which you would like the
	program to output the data to (does not need to exist).

	* Use right arrow key to "swipe right" on truly damaged solar panels
	* Use left arrow key to "swipe left" on not damaged solar panels
	* If you make a mistake, use the up arrow key to go back.
	* Outputs: a JSON file with a list of the right-swiped images
