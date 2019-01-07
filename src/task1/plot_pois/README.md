Example Module
---
# Description
Place two JSON files as follows. **Filenames are relative to the script!**

## Input
###map.json
```
{
	topleft: {
		lat: 123.456,
		long: 123.456
	},
	bottomright: {
		lat: 123.456,
		long: 123.456
	},
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

# Usage
You can type `plot_pois.py -h` to get more information.
```
usage: plot_pois.py [-h] [-im INPUTMAP] [-id INPUTDAMAGED] [-i OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -im INPUTMAP, --inputmap INPUTMAP
                        The location/filename of the input map json file.
  -id INPUTDAMAGED, --inputdamaged INPUTDAMAGED
                        The location/filanem of the damaged panels JSON file.
  -i OUTPUT, --output OUTPUT
                        The output file name.
```

