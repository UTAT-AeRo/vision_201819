### Description

This module takes a folder contain unflattened images and by use of a GUI utility
allows the user to create a folder containing images of only the panel as if it
were being viewed flat on.

### Usage
The program takes two arguments

```--input```: The path to the input json.
```--output```: The path to the folder where the output json and all images will
be saved

Example Call

```python flattener.py --input test.json --output test_folder```


### Input Json format 1
```
{
    "../../task1/common/test/2018-05-25_16-22-29-018.bmp": [[408, 304], [596, 302], [619, 158], [472, 188], [874, 256], [738, 392]],
    "../../task1/common/test/2018-05-25_16-22-29-685.bmp": [121, 312]
}
```

### Input Json format 2
```
[
    "../../task1/common/test/2018-05-25_16-22-29-018.bmp",
    "../../task1/common/test/2018-05-25_16-22-29-685.bmp"
]
```


### Output Json

```
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
