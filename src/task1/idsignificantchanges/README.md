# Overview
Corresponds to:
https://trello.com/c/l0EsBnPP/34-id-significant-changes

to use example data, run:
`python idsignificantchanges.py --map=inputmap.json --photos=inputsurveyphotos.json`

more generally:</br>
`python idsignificantchange.py --map=[path to reference map json without quotations] --photos=[path to surveyphotos json without quotations]`
</br>

1. 2 windows will launch. One will contain the map, the other will be the first image in the list of images in `surveyphotos.json`
</br>
<p align="left">
  <img src="https://cdn.discordapp.com/attachments/511941623299571713/549033009215700992/unknown.png" width=500 align= "center">
</p>
</br>
2. Cycle through images on the second window with Next, Previous. Then when ready, click location on map to add label.
<p align="left">
  <img src="https://cdn.discordapp.com/attachments/511941623299571713/549033235871563787/unknown.png" alt="Image of evaluation_metrics.csv" width=500 align = "center">
</p>
</br>
3. Once you've cycled through all of the survey images, simply close the map window. This will write out a `idsignificantchanges.json`
</br>

```
{
"damaged": [
	{"lat": 43.66520317216643,
	"long": -79.39335502006688,
	"message": "something happened",
	"filename": "images/2019-02-22_18-26-59-161.jpg"}
	]
}
```

# Sample Input

sample reference map json assumes map is oriented north
```
{"topleft": {"long":-79.393549, "lat" :43.665497},
 "bottomright": {"long":-79.391549, "lat":43.664320},
 "filename": "test.jpg"
}
```

sample survey images are
```
["images/2019-02-22_18-26-59-161.jpg",
  "images/2019-02-22_18-26-59-411.jpg",
  "images/2019-02-22_18-26-59-911.jpg",
  "images/2019-02-22_18-27-00-911.jpg",
  "images/2019-02-22_18-27-06-411.jpg"
]
```

# Output
some `idsignificantchanges.json` containing:
```
{
   "damaged":[
      {
         "lat":XX.XXX,
         "long":XX.XXX,
		     "message":"message",
         "filename":"absoluate/path/to/img.jpg"
      },
      etc...
   ]
}
```
