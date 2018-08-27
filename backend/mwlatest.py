# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 10:53:00 2016

@author: tanner

RAWS FETCHER
"""

import urllib.request
import json
import csv

baseurl="http://api.mesowest.net/v2/stations/latest?"
dtoken="33e3c8ee12dc499c86de1f2076a9e9d4"

def stationUrlBuilder(token,stid,svar,within,spdUnits,tempUnits):
    tokfull="&token="+token
    stidfull="stid="+stid
    svarfull="&vars="+svar
    if svar=="":
#        print "urlBuilder: downloading all variables for station"
        svarfull=""
    timesand="&within="+str(within)
    if within=="":
        timesand=""
    url=baseurl+stidfull+svarfull+timesand+tokfull
    return url
def radiusUrlBuilder(token,stid,radius,limit,svar,within):
    tokfull="&token="+token
    stidfull="&radius="+stid+","+radius
    svarfull="&vars="+svar
    if svar=="":
        svarfull=""
    timesand="&within="+str(within)
    if within=="":
        timesand=""
    limiter="&limit="+limit
    url=baseurl+stidfull+svarfull+limiter+timesand+tokfull
    return url
def latlonBuilder(token,lat,lon,radius,limit,svar,within,spdUnits,tempUnits):
    tokfull="&token="+token
    stidfull="&radius="+lat+","+lon+","+radius
    svarfull="&vars="+svar
    if svar=="":
        svarfull=""
    timesand="&within="+str(within)
    if within=="":
        timesand=""
#    limiter="&limit="+limit
    unitsBase="&units="
    units=""
    if spdUnits=="english":
        units=units+"speed|mph,"
    if tempUnits=="english":
        units=units+"temp|F,"
        units=units+"precip|in,"
    units=unitsBase+units+"metric"
  
    url=baseurl+stidfull+svarfull+"&status=active"+"&network=1,2"+units+timesand+tokfull
#    url=baseurl+stidfull+svarfull+"&status=active"+units+timesand+tokfull    
    return url
    
def readData(url):
    new=urllib.request.urlopen(url)
    response=new.read()
    json_string=response.decode()
    a=json.loads(json_string)
    return a
    
    
def getRAWSData(Lat,Lon,Radius):
    """
    used mesonet api from mwlatest to fetch 
    weather station data
    """
    url=latlonBuilder(dtoken,
                               str(Lat),str(Lon),str(Radius),"",
#    "relative_humidity,air_temp,wind_speed,wind_direction,wind_gust,precip_accum_one_hour",
   "",
    "","english","english")
    response=readData(url)
    return response
    
    
    
#a = getRAWSData(47,-114,30)
#b = a['STATION']
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     