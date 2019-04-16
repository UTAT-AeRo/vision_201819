Remove Duplicate images
---
# Description
This module is intended to automatically filter duplicate images of panels. In other words after this is module
 is run all panels will be list under one and only one image.
If a panel is in multiple images then the entry for it should be kept in the image where it is most central.


# Prerequisites
- Python 3

# Usage
`python remove_duplicated.py in.json out.json height width threshold`

The height and width of the image should be both 5120.
threshold is the threshold distance for two similar gps locations.
