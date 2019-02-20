###
Allows for the annotation of images of panels.


### USAGE
```
usage: damageselector.py [-h] [--input INPUT] [--output OUTPUT]
                         [--line_width LINE_WIDTH] [--text_size TEXT_SIZE]
                         [--decimal_places DECIMAL_PLACES]

Flatten a list of panels

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         The path to the jason contain
  --output OUTPUT       The folder to save output new images
  --line_width LINE_WIDTH
                        The size of the dots used to mark and select panel
                        corners.
  --text_size TEXT_SIZE
                        The size of the text on the final cv image
  --decimal_places DECIMAL_PLACES
                        The number of decimal points for lengths and areas

Process finished with exit code 0
```
s
### Input Format
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
