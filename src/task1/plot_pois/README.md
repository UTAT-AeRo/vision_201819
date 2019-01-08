Plot POIs Module v2
---
# Description
The purpose of this program is to mark a map with points of interest (POI). This version takes a series of known point coordinates as input and a series of damaged panel locations and produces a final output map with the POIs.

## Input
###map.json
```
{
	"points" : [
		{
			"lat":
			"long":
			"x":
			"y":
		},
		...
	],
	filename: "map.jpg"
}
```

###damaged.json**
```
{
	damaged: [
		{
			lat: 123.456,
			long: 123.456,
			filename: "img_0124.jpg"
		},
		{
			lat: 123.456,
			long: 123.456,
			filename: "img_0124.jpg"		
		},
		...
	]
}
```
## Output
Unless otherwise provided, the script defaults to the following output name: usc_utataero_YYYYMMDD_HHMMSS.jpg


# Prerequisites
- Python 3
- numpy
- opencv

# Usage
You can type `plot_pois.py -h` to get more information.
```
usage: plot_pois.py [-h] [-im INPUTMAP] [-id INPUTDAMAGED] [-o OUTPUT]
                    [-pi PINIMAGE] [-ps PINSCALE]

optional arguments:
  -h, --help            show this help message and exit
  -im INPUTMAP, --inputmap INPUTMAP
                        The location/filename of the input map json file.
  -id INPUTDAMAGED, --inputdamaged INPUTDAMAGED
                        The location/filanem of the damaged panels JSON file.
  -o OUTPUT, --output OUTPUT
                        The output file name.
  -pi PINIMAGE, --pinimage PINIMAGE
                        The file name of the marker image.
  -ps PINSCALE, --pinscale PINSCALE
                        The scale you'd like for the pin image.
```