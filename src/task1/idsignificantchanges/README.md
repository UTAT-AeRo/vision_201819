# Overview
Corresponds to:
https://trello.com/c/l0EsBnPP/34-id-significant-changes

to use example data, run:
`python idsignificantchanges.py --map=inputmap.json --photos=inputsurveyphotos.json`

more generally:</br>
`python idsignificantchange.py --map=[path to reference map json without quotations marks] --photos=[path to surveyphotos json without quotations marks]`

# Input 

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
  "images/2019-02-22_18-27-06-411.jpg",
  "images/2019-02-22_18-27-09-161.jpg",
  "images/2019-02-22_18-27-10-411.jpg",
  "images/2019-02-22_18-27-16-411.jpg",
  "images/2019-02-22_18-27-20-661.jpg",
  "images/2019-02-22_18-27-26-911.jpg",
  "images/2019-02-22_18-27-28-411.jpg",
  "images/2019-02-22_18-27-29-661.jpg",
  "images/2019-02-22_18-27-32-411.jpg",
  "images/2019-02-22_18-27-34-911.jpg",
  "images/2019-02-22_18-42-47-235.jpg",
  "images/2019-02-22_18-42-56-235.jpg",
  "images/2019-02-22_18-43-01-485.jpg",
  "images/2019-02-22_18-43-05-485.jpg",
  "images/2019-02-22_18-43-10-485.jpg",
  "images/2019-02-22_18-43-19-485.jpg",
  "images/2019-02-22_18-43-31-235.jpg",
  "images/2019-02-22_18-43-40-235.jpg"
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
