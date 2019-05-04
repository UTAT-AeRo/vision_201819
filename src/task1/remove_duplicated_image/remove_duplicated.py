import sys
import json
import math





#set threshold of deleting the gps location


#setting command lines. h is height of the image, w is width of the image
input_json_file=sys.argv[1]
output_json_file=sys.argv[2]
h=int(sys.argv[3])
w=int(sys.argv[4])
threshold=float(sys.argv[5])

print(threshold)

#extracting json info
with open(input_json_file) as file:
   input_data=json.load(file)


panels=set()
i=0
for files in input_data:
   for gps_num in range(0,len(files["gps"]),1):
      panels.add(((files["gps"][gps_num][0], files["gps"][gps_num][1]),
                  (files["pixels"][gps_num][0], files["pixels"][gps_num][1]), files["file"]))



visited=set()
centers=set()












# #calculate distance between two gps locations
def dist(a,b):
   #pythagorean therom
   result=math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))
   return result


# input will be a set of tuples: {((12,34),(23,23),"image1"),((4543,23),(34,65),"image2")}
# output will be only one:{((12,34),(23,23),"image1")}
def calc_most_central(in_group):
   #if there's only one grouped gps location
   if len(in_group)==1:
      return in_group
   else:

      cen=set()
      #set a large max dist, so the first dist always overwrite this
      maxdist=999999
      for gps in in_group:
         dist = math.sqrt((h / 2 - gps[1][1]) * (h / 2 - gps[1][1]) + (w / 2 - gps[1][0]) * (w / 2 - gps[1][0]))
         if dist<maxdist:
            maxdist=dist
            cen={gps}


      return cen


##go through all the panels and put the ones with close gps index in a group
for panel_1 in panels:

   if panel_1 not in visited:
      visited.add(panel_1)
      group=set()
      group.add(panel_1)

      for panel_2 in panels:
         if ((panel_2 not in visited) and (dist(panel_1[0], panel_2[0]) < threshold)):
            group.add(panel_2)



   #find the most central one in the group
   temp=calc_most_central(group)

   #add to centers, if it doesn't exist in centers
   centers=centers|temp





json_entery_for = dict()

for centergps in centers:
   (gps, pixels, path) = centergps
   # concatenate gps and pixels
   if path in json_entery_for:
      json_entery_for[path]['gps'].append(gps)
      json_entery_for[path]['pixels'].append(pixels)


   # create a path called "image path", put json output in it
   else:
      json_entery_for[path] = {'file': path, 'gps': [gps], 'pixels': [pixels]}

   final_json = list(json_entery_for.values())

with open(output_json_file, 'w', encoding='utf8') as outfile:
   json.dump(final_json,outfile)
