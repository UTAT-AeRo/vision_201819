### Description

This module takes a folder contain unflattened images and by use of a GUI utility
allows the user to create a folder containing images of only the panel as if it
were being viewed flat on.

### Usage
```
usage: imageflattener.py [-h] [--input INPUT] [--output OUTPUT]
                         [--outputjson OUTPUTJSON] [--dot_size DOT_SIZE]

Flatten a list of panels

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         The path to the json containing the images
  --output OUTPUT       The folder to save the new images and by default the
                        json as well
  --outputjson OUTPUTJSON
                        The path to where the json will be saved
  --dot_size DOT_SIZE   The size of the dots used to mark and select panel
                        corners.
```

Example Call

```python flattener.py --input test.json --output test_folder```


### Input Format
```json
[
    {
        "file": "img1.bmp",
        "gps": [[12, 12], [321, 432]],
        "pixels": [[12, 12], [2250, 3213]]
    },
    {
        "file": "img2.bmp",
        "gps": [[14232, 14232]],
        "pixels": [[12, 12]]
    }
]
```

### Output Json

```json
[
    {
        "file": "img1_flat.bmp",
        "gps": [12, 12],
        "dims": [20.0, 20.0]
    },
    {
        "file": "img1_flat_1.bmp",
        "gps": [321, 432],
        "dims": [20.0, 20.0]
    },
    {
        "file": "img2.bmp",
        "gps": [14232, 14232],
        "dims": [12.0, 12.0]
    }
]
```

The first element in the list being the length of the smaller edge of the panel
and the second being the length of the longer edge.


### Notes on usage

**Buttons**
- The reload button resets the image
- The save button saves the image to the output folder and resets your view
- The next button loads the next image or exits the program if there are no images left
