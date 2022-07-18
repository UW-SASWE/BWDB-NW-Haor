import ee
import folium
#~ %tensorflow_version 2.x
#~ import tensorflow as tf
import numpy as np
import pandas as pd
from datetime import datetime as dt
# from StringIO import StringIO
import math, time
try:
    #ee.Authenticate()
    ee.Initialize()
except Exception as e:
  ee.Authenticate()
  ee.Initialize() 
# from ee_plugin import Map 
import datetime
import math,os,time

import pickle
import os.path
import io,sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

import pickle
import os.path
import io
import shutil
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import datetime, time
	
DEM = ee.Image("USGS/SRTMGL1_003")

l7Raw = ee.ImageCollection('LANDSAT/LE07/C01/T1')
l7TOA = ee.ImageCollection("LANDSAT/LE07/C01/T1_TOA")
res = ee.FeatureCollection("users/climateClass/grand_tempwork/GRanD_reservoirs_v1_1")
dams = ee.FeatureCollection("users/climateClass/grand_tempwork/GRanD_dams_v1_1")
asia_res = ee.FeatureCollection("users/climateClass/grand_tempwork/GRanD_asia_ds_buffer")
usa_ds_res = ee.FeatureCollection("users/climateClass/grand_tempwork/nhd_ds_buffer_filt")
res_usgs = ee.FeatureCollection("users/climateClass/grand_tempwork/GRanD_reservoirs_usgs_nonan")
s1 = ee.ImageCollection("COPERNICUS/S1_GRD")

ne_bd = ee.Geometry.Polygon([[[90.42864448393777, 24.908543492090704],
          [90.51434642638162, 24.23021252443603],
          [90.92500335539773, 23.656235335961178],
          [91.15502960051492, 23.653837456446542],
          [91.38535625304178, 24.051633600999917],
          [91.90514690245584, 24.312173229538068],
          [92.2242654022117, 24.620487117272614],
          [92.45922691191629, 24.942985900973305],
          [92.1568883117576, 25.123368679140967],
          [91.60988933409647, 25.178880377968145],
          [90.52091247405008, 25.189288436305866]]])
nw_bd = ee.Geometry.Polygon(
        [[[89.62318889154137, 23.891909229102687],
          [89.68910686029137, 24.293079416965313],
          [89.54079143060387, 24.912389910245217],
          [89.59572307122887, 25.459190685859696],
          [89.37599650872887, 25.79267100043818],
          [89.09035197747887, 25.921194697134766],
          [89.06288615716637, 26.103852360624437],
          [88.82118693841637, 26.21232466050638],
          [88.60695353997887, 26.23203605313372],
          [88.59596721185387, 26.374843624563336],
          [88.23341838372887, 26.069317311866797],
          [88.16200725091637, 25.842119724496545],
          [88.29933635247887, 25.88660591209792],
          [88.33778850091637, 25.770472156450655],
          [88.59596721185387, 25.537743883657065],
          [88.80470744622887, 25.547656454104033],
          [88.89809123529137, 25.38895712248733],
          [89.04640666497887, 25.314494843945646],
          [89.00795451654137, 25.165432978613307],
          [88.64540568841637, 25.155489026054713],
          [88.51906291497887, 25.06098108418934],
          [88.12355510247887, 24.72214580905657],
          [88.24138110207488, 24.566865321969708],
          [88.40617602394988, 24.451906903155354],
          [88.65336840676238, 24.396889658265557],
          [88.77421801613738, 24.28678329458654],
          [88.81816332863738, 24.17156992494263],
          [89.02690356301238, 24.18159261572658],
          [89.08732836769988, 24.12645808129721],
          [89.13676684426238, 24.01110001243043]]])


AREA_THRESHOLD = 0.75
# Initialize date range

i=-1#35
edate =  datetime.datetime.now() + datetime.timedelta(days=i)   # # 
sdate = edate  + datetime.timedelta(days=-3)   ## CHANGE FOR MORE DAYS TO MOSAIC

print("Looking from {} to {}...".format(sdate.strftime("%Y-%m-%d"),edate.strftime("%Y-%m-%d")))

Date_End = ee.Date(edate)  #ee.Date(datttte()) 
Date_Start = ee.Date(sdate) # ee.Date('1987-01-01')
  
n_days = Date_End.difference(Date_Start,'day').round();
gap = -10     ## CHANGE FOR MORE DAYS TO MOSAIC
dates = ee.List.sequence(0,n_days, 1);   #only one day list
def make_datelist(n):
  return Date_Start.advance(n,'day') 

dates = dates.map(make_datelist);

for dt in dates.getInfo():
	print(ee.Date(dt.get('value')).format('Y-MM-dd').getInfo())

ROI = nw_bd  ##selres.geometry().buffer(buffDist)    # for upstream from GRanD

#//*******************  SENTINEL SAR 1 PROCESSING  ***********************************************************

# Threshold for look angle used to remove erroneous data at far edges of images
angle_threshold_1 = ee.Number(45.4);
angle_threshold_2 = ee.Number(31.66)

# Define focal median function
def focal_median(img):
  fm = img.focal_max(30, 'circle', 'meters')
  fm = fm.rename("Smooth")
  return img.addBands(fm)
  
def smoothing(img):
  # Define a boxcar or low-pass kernel.
  boxcar = ee.Kernel.circle(radius = 1, units = 'pixels', magnitude = 1)

  # Smooth the image by convolving with the boxcar kernel.
  smooth = img.convolve(boxcar);
  smooth = smooth.rename("Smooth")
  return img.addBands(smooth)

  
  
# Define masking function for removing erroneous pixels
def mask_by_angle(img):
  angle = img.select('angle');
  vv = img.select('VV');
  mask1 = angle.lt(angle_threshold_1);
  mask2 = angle.gt(angle_threshold_2);
  vv = vv.updateMask(mask1);
  return vv.updateMask(mask2);
  

def calcWaterPix(img):
  sum = img.reduceRegion(reducer=ee.Reducer.sum(), geometry=ROI, scale=10, maxPixels=1e13);
  return img.set("water_pixels", sum.get('Class'));

# Apply median calculation on moving date window. 
def  detectWaterSAR(d):
  end = ee.Date(d);
  start = ee.Date(d).advance(gap ,'day');
  date_range = ee.DateRange(start,end);
  
  S1 = s1\
    .filterDate(date_range)\
    .filterBounds(ROI)\
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
  vv = S1.map(mask_by_angle)
  vv = vv.map(smoothing); #focal_median);
  vv_median = vv.select("Smooth").median();
   
  clas = vv_median.lt(-13);
  mask = vv_median.gt(-32);
  clas  = clas.mask(mask); 
  
  #~ median_class = clas.addBands(vv_median).rename(['Class','Median']).clip(ROI) 
  #~ waterSAR = median_class.lt(-13)
  #~ numwaterpix = calcWaterPix(median_class)
  #~ waterArea = ee.Number(numwaterpix.get('water_pixels'))
  #~ waterArea = waterArea.multiply(.0001) 
  #~ return [waterSAR,waterArea]		

  sardate=ee.Date(S1.first().get('system:time_end'))
  return clas.addBands(vv_median).rename(['Class','Median']).clip(ROI).set("system:time_start", ee.Date(S1.first().get('system:time_start')).format('Y-MM-dd'));

### Sentinel ###

#~ try: 
  
resSAR = ee.ImageCollection(dates.map(detectWaterSAR))
#~ resSAR = resSAR.map(calcWaterPix)
#~ wc = ee.Array(resSAR.aggregate_array('water_pixels'))
#~ wc = wc.multiply(0.0001)
#~ d = (resSAR.aggregate_array('system:time_start'))


#~ areas = np.column_stack((d.getInfo(), wc.getInfo())).tolist()


# #### Check fraction of area covered 
imgafter = resSAR.median().select("Median").lt(-13).clip(ROI)
water_area = ee.Number(imgafter.reduceRegion(reducer=ee.Reducer.sum(), geometry=ROI, scale=10, maxPixels=1e13).get('Median')).multiply(0.0001);
print('water_area',water_area.getInfo())
area_after = imgafter.reduceRegion(reducer=ee.Reducer.count(), geometry=ROI, scale=10, maxPixels=1e13);
print('after',area_after.getInfo())

zeroimg = ee.Image(0)
imgbefore = zeroimg.where(imgafter.lt(-13),ee.Image(1)).clip(ROI)
area_before = imgbefore.reduceRegion(reducer=ee.Reducer.count(), geometry=ROI, scale=10, maxPixels=1e13);
print('before',area_before.getInfo())

area_ratio = ee.Number(area_after.get('Median')).divide(area_before.get('constant'))
print('ratio',area_ratio.getInfo())


#### CHECK OF AREA_THRESHOLD
if(area_ratio.getInfo() < AREA_THRESHOLD):
  print('Not enough area covered by SAR, fraction covered: {}'.format(area_ratio.getInfo()))

else:
  print('Exporting processed SAR, fraction covered: {}'.format(area_ratio.getInfo()))

  with open('HaorArea_smooth.csv', 'a') as f:
      f.write("{},{}\n".format(edate.strftime("%Y-%m-%d"),water_area.getInfo()))


  ############################################################################################
  ### export to drive

  sarlist = resSAR.toList(resSAR.size().getInfo())


  sarexp = ee.Image(sarlist.get(i)).select('Median')

  latest_day = edate.strftime("%Y-%m-%d") #sarexp.get('system:time_start')).getInfo()
  print('--Latest day',latest_day)

  print('--Exporting SAR area map {} to Drive'.format(latest_day))

  task_config = {
    'fileNamePrefix': 'Barind_SAR_Haors_Smooth_'  + latest_day,
    'crs': 'EPSG:4326',
    'scale': 10,
    'maxPixels': 1e13,
    'fileFormat': 'GeoTIFF',
    'skipEmptyTiles': True,
    'region': ROI,
    'folder': 'HaorStorage_GEE_exports'
    }

  task = ee.batch.Export.image.toDrive(imgafter, str('sar-export'), **task_config)
  task.start()
  import time
  while task.active():
    time.sleep(30)
    print(task.status())



  ############################################################################################
  ####  Download fromDrive 

  import pickle
  import os.path
  import io
  import shutil
  import requests
  from mimetypes import MimeTypes
  from googleapiclient.discovery import build
  from google_auth_oauthlib.flow import InstalledAppFlow
  from google.auth.transport.requests import Request
  from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
  import datetime, time

  day = latest_day
  print('Downloading',day)

  # Define the scopes
  SCOPES = ['https://www.googleapis.com/auth/drive']



  # Variable self.creds will
  # store the user access token.
  # If no valid token found
  # we will create one.
  creds = None

  # The file token.pickle stores the
  # user's access and refresh tokens. It is
  # created automatically when the authorization
  # flow completes for the first time.

  # Check if file token.pickle exists
  if os.path.exists('token.pickle'):

    

      # Read the token from the file and
      # store it in the variable self.creds
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)

  # If no valid credentials are available,
  # request the user to log in.
  if not creds or not creds.valid:


      # If token is expired, it will be refreshed,
      # else, we will request a new one.
    if creds and creds.expired and creds.refresh_token:
	    creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the access token in token.pickle
    # file for future usage
    with open(r'token.pickle', 'wb') as token:
        pickle.dump(creds, token)

  # Connect to the API service
  service = build('drive', 'v3', credentials=creds)

  # request a list of first N files or
  # folders with name and id from the API.
  results = service.files().list(
      pageSize=100, fields="files(id, name)").execute()
  items = results.get('files', [])
  for file in results.get('files', []):
    if('Barind_SAR_Haors_Smooth_'+day in file.get('name')):

      print('Found latest map: %s (%s)' % (file.get('name'), file.get('id')))
      file_id = file.get('id')
      file_nm = file.get('name')
  # print a list of files
  print(file_id,file_nm)
  # print("Here's a list of files: \n")
  # print(*items, sep="\n", end="\n\n")


  request = service.files().get_media(fileId=file_id)
  fh = io.BytesIO()

  # Initialise a downloader object to download the file
  downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
  done = False

  try:

      # Download the data in chunks
    while not done:
	    status, done = downloader.next_chunk()

    fh.seek(0)
      
      # Write the received data to the file
    with open('Processed/'+file_nm, 'wb') as f:
        shutil.copyfileobj(fh, f)

    print("File Downloaded")
      # Return True if file Downloaded successfully
   
  except:
      
      # Return False if something went wrong
    print("Something went wrong.")
