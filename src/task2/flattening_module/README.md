### Description

This module takes a folder contain unflattened images and by use of a GUI utility
allows the user to create a folder containing images of only the panel as if it
were being viewed flat on.

### Usage
```
usage: imageflattener.py [-h] [--input INPUT] [--output OUTPUT]
                         [--dot_size DOT_SIZE]

Flatten a list of panels

optional arguments:
  -h, --help           show this help message and exit
  --input INPUT        The path to the jason contain
  --output OUTPUT      The folder to save output json and new images
  --dot_size DOT_SIZE  The size of the dots used to mark and select panel
                       corners.
```

Example Call

```python flattener.py --input test.json --output test_folder```


### Input Json format 1
```json
{
    "../../task1/common/test/2018-05-25_16-22-29-018.bmp": [[408, 304], [596, 302], [619, 158], [472, 188], [874, 256], [738, 392]],
    "../../task1/common/test/2018-05-25_16-22-29-685.bmp": [121, 312]
}
```

### Input Json format 2
```json
[
    "../../task1/common/test/2018-05-25_16-22-29-018.bmp",
    "../../task1/common/test/2018-05-25_16-22-29-685.bmp"
]
```


### Output Json

```json
{
    "test/2018-05-25_16-22-29-018_flat.bmp": [123.0, 123.0],
    "test/2018-05-25_16-22-29-018_flat_1.bmp": [23.0, 123.0],
    "test/2018-05-25_16-22-29-018_flat_2.bmp": [111.0, 232.0],
    "test/2018-05-25_16-22-29-685_flat.bmp": [111.0, 232.0]
}
```

The first element in the list being the length of the smaller edge of the panel
and the second being the length of the longer edge.


### Notes on usage

**Buttons**
- The reload button resets the image
- The save button saves the image to the output folder and resets your view
- The next button loads the next image or exits the program if there are no images left
