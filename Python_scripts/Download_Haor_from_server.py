# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 19:46:35 2022

@author: skhan7
"""

import datetime
import urllib
import urllib2
import subprocess
# import requests

#import h5py
# import pandas as pd
import os
import shutil
#import numpy as np
# import rasterio
#import csv
import glob
import paramiko
from scp import SCPClient
# import wget
# from urllib import request

homedir=r"D:\SASWMS_Shahzaib\barind\Web"
class HaorStorageProcessor():
    def __init__(self,nd):
        self.todaydate = datetime.date.today()
        self.noforedays = 3
        self.swatstartdate = datetime.datetime.combine(datetime.date(2017,1,1), datetime.time(0,0))
        self.forestartdate =  datetime.datetime.combine(self.todaydate, datetime.time(0,0)) + datetime.timedelta(days=nd)  #-2
        
        self.foreenddate = self.forestartdate + datetime.timedelta(days=self.noforedays)
#        self.foreenddate = datetime.datetime.combine(self.todaydate, datetime.time(0,0)) + datetime.timedelta(days=self.noforedays)
        
#        self.imergprcpdate = datetime.datetime.combine(self.todaydate, datetime.time(0,0)) + datetime.timedelta(days=-1)
        self.rasstartdate = self.forestartdate + datetime.timedelta(days=-8)
        # self.visstartdate = self.forestartdate + datetime.timedelta(days=-21)
        
        # self.conn = sqlite3.connect('Insituwaterlevel.db')
        print self.todaydate, self.forestartdate, self.foreenddate

    def download_SAR(self):
        text = urllib.URLopener()
        enddate = self.forestartdate 
        preciptime = (enddate + datetime.timedelta(days=-1)).strftime('%Y%m%d') 
        dwntime = (enddate + datetime.timedelta(days=-1)).strftime('%Y-%m-%d') 
        wrftime=enddate.strftime('%Y%m%d')
        # IMERG
        print "Downloading SAR: Barind_SAR_Haors_Smooth_" + dwntime + ".tif" 
        try:
        # URL = "http://128.95.45.89/barind/maps/Barind_SAR_Haors_Smooth_" + dwntime + ".tif" 
        # response = wget.download(URL, "C:\Users\skhan7\Desktop\Research\LOCSS\Tool\NW_Tool\To_cluster\attachments\sardata\Barind_SAR_Haors_" + dwntime + ".tif" )
        # text.retrieve("http://128.95.45.89/barind/maps/Barind_SAR_Haors_Smooth_" + dwntime + ".tif" , "C:\Users\skhan7\Desktop\Research\LOCSS\Tool\NW_Tool\To_cluster\attachments\sardata\Barind_SAR_Haors_" + dwntime + ".tif")
        # text.retrieve('http://128.95.45.89/barind/maps/Barind_SAR_Haors_Smooth_2022-06-25.tif','haha.tif')
        # request.urlretrieve("http://128.95.45.89/barind/maps/Barind_SAR_Haors_Smooth_" + dwntime + ".tif" , "C:\Users\skhan7\Desktop\Research\LOCSS\Tool\NW_Tool\To_cluster\attachments\sardata\Barind_SAR_Haors_" + dwntime + ".tif" )

            output_address = r"D:\SASWMS_Shahzaib\barind\ProcessHaorsAutom_V97\for_redistribution_files_only\sardata\Barind_SAR_Haors_Smooth_" + dwntime + ".tif"
            with open(output_address,'wb') as f:
                f.write(urllib2.urlopen("http://128.95.45.89/barind/maps/Barind_SAR_Haors_Smooth_" + dwntime + ".tif").read())
                f.close()
            print "Download Complete!"
        except:
            print "SAR not available"
            
        
        # URL = "https://instagram.com/favicon.ico"
        # response = request.urlretrieve("https://instagram.com/favicon.ico", "instagram.ico")
if __name__ == '__main__':
#    for nd in range(-2,-1):  #(-53,0):
    nd= 0 #0
    forecast = HaorStorageProcessor(nd)
    forecast.download_SAR()
