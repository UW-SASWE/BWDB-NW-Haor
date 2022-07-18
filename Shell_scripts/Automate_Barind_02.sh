#!/bin/bash


cd /home/saswms/ShahzaibWork/NW_BWDB_Tool/

nn=4
i=$(date +"%Y" -d "$nn days ago")	 ## "today")			## Year
j=$(date +"%m" -d "$nn days ago")	 ## "today")			## Month
k=$(date +"%d" -d "$nn days ago")	 ##"today")			## Day
j=$((10#$j)) # converting to decimal form octal in case of 08 or 09
k=$((10#$k))

ym=$i$(printf %02d $j) #-$(printf %02d $k)
ymd=$i$(printf %02d $j)$(printf %02d $k)
echo $ymd
 
 
## after Matlab processing

## process png
cd /home/saswms/ShahzaibWork/NW_BWDB_Tool/Processed
wget --user=saswms --password=******  ftp://128.95.45.89/../../opt/lampp/htdocs/barind/maps/Processed_tif/Processed_Haor_Barind_${ymd}.tif

gdaldem color-relief Processed_Haor_Barind_${ymd}.tif  ../water_binary_palette.txt -alpha cProcessed_Haor_Barind_${ymd}.tif
gdal_translate -of png cProcessed_Haor_Barind_${ymd}.tif Processed_Haor_Barind_${ymd}.png
gdal_translate -of png cProcessed_Haor_Barind_${ymd}.tif Processed_Haor_Barind.png     ## for latest day label

## send to server

wput *${ym}*.png ******128.95.45.89/../../opt/lampp/htdocs/barind/maps/Processed_png/
wput Processed_Haor_Barind.png -u *******128.95.45.89/../../opt/lampp/htdocs/barind/maps/Processed_png/
rm cProcessed_Haor_Barind_${ymd}.tif
