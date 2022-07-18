#!/bin/bash


cd /home/saswms/ShahzaibWork/NW_BWDB_Tool/

nn=1
i=$(date +"%Y" -d "$nn days ago")	 ## "today")			## Year
j=$(date +"%m" -d "$nn days ago")	 ## "today")			## Month
k=$(date +"%d" -d "$nn days ago")	 ##"today")			## Day
j=$((10#$j)) # converting to decimal form octal in case of 08 or 09
k=$((10#$k))

ym=$i-$(printf %02d $j) #-$(printf %02d $k)
ymd=$i-$(printf %02d $j)-$(printf %02d $k)
echo $ymd
 

ip=$(date +"%Y" -d "10 days ago")	 ## "today")			## Year
jp=$(date +"%m" -d "10 days ago")	 ## "today")			## Month
kp=$(date +"%d" -d "10 days ago")	 ##"today")			## Day
jp=$((10#$jp)) # converting to decimal form octal in case of 08 or 09
ymp=$ip-$(printf %02d $jp) #-$(printf %02d $k)



## Download and process sar delineation
/home/saswms/anaconda2/bin/python3 SAR_Area_Haors_drive_error.py

cd /home/saswms/ShahzaibWork/NW_BWDB_Tool/Processed
wput *Smooth*${ym}*.tif ******@128.95.45.89/../../opt/lampp/htdocs/barind/maps/
wput *Smooth*${ymp}*.tif *******@128.95.45.89/../../opt/lampp/htdocs/barind/maps/  # for prev month date
