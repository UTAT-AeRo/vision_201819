import sys
import json
import math
import copy
import cv2

#set threshold of deleting the gps location


#setting command lines. h is height of the image, w is width of the image
input_json_file=sys.argv[1]
output_json_file=sys.argv[2]
h=int(sys.argv[3])
w=int(sys.argv[4])
threshold=float(sys.argv[5])
#output_json_file=sys.argv[2]


#extracting json info
with open(input_json_file) as file:
   input_data=json.load(file)


# #calculate distance between two gps locations
def dist(a,b):
   #pythagorean therom
   result=math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))
   return result

#gps coordinate with most central pixel
# input will be [[file#,gps#],[file#,gps#]]; output will be[file#,gps#]
def calc_most_central(in_ggps):
   #if there's only one grouped gps location
   if len(in_ggps)==1:
      return in_ggps[0]
   else:
      #creating a list of central_coefficient for each gps locations
      cen_c=[]
      for i in range(0,len(in_ggps),1):
         #extract image size from input_data[file#][file_name]; h:height,w:width


         #calculate distance
         pixel=input_data[in_ggps[i][0]]["pixels"][in_ggps[i][1]]
         dist=math.sqrt((h/2-pixel[0])*(h/2-pixel[0])+(w/2-pixel[1])*(w/2-pixel[1]))
         area=pixel[0]*pixel[1]
         cen_c=cen_c+[dist/area]
      mc_index=cen_c.index(min(cen_c))
      return in_ggps[mc_index]



final_json = copy.deepcopy(input_data)
#loop for first picture file
for fp_i in range(0, (len(input_data)) - 1, 1):
#loop for first picture gps locations in the file
   for fp_gps_i in range(0, len(input_data[fp_i]["gps"])):
      grouped_gps=[[fp_i, fp_gps_i]]
#loop for second picture file
      for sp_i in range((fp_i) + 1, len(input_data)):
#loop for second picture gps locations in the file
         for sp_gps_i in range(0, len(input_data[sp_i]["gps"])):
            if dist(input_data[fp_i]["gps"][fp_gps_i], input_data[sp_i]["gps"][sp_gps_i])<threshold:
               grouped_gps=grouped_gps+[[sp_i, sp_gps_i]]

      #remove the most central from grouped gps
      most_central=calc_most_central(grouped_gps)
      grouped_gps.remove(most_central)
      #set duplicated gps location and pixel in final json file to zero. grouped gps looks like[[file#,gps#],[file#,gps#]]
      for duplicated_gps in grouped_gps:
         final_json[duplicated_gps[0]]["gps"][duplicated_gps[1]]=0
         final_json[duplicated_gps[0]]["pixels"][duplicated_gps[1]] = 0


def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]
#remove zeros from final_json
for file_num in range(0,len(final_json),1):
   final_json[file_num]["gps"]=remove_values_from_list(final_json[file_num]["gps"],0)
   final_json[file_num]["pixels"]=remove_values_from_list(final_json[file_num]["pixels"],0)


with open(output_json_file, 'w', encoding='utf8') as outfile:
   json.dump(final_json,outfile)