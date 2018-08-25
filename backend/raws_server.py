#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 14:22:36 2018

@author: tanner

RAWS SERVER - Replacement for meso-server.py
"""

#global libraries
import getpass
import time
import sys

#local files
import mwlatest
import RAWS

if getpass.getuser()=='tanner':
    tDir='/home/tanner/src/nu-weather/RAWS-Locator/shiny/data/'
if getpass.getuser()=='tfinney':
    tDir='/home/tfinney/src/fs/nu-weather/RAWS-Locator/shiny/data/'
else:
    tDir='/srv/shiny-server/raws/raws-table/data/'
    
tFile=tDir+'nu-'+str(int(time.time()))+'.csv'
  
    
def getRAWSData(Lat,Lon,Radius):
    """
    used mesonet api from mwlatest to fetch 
    weather station data
    """
    url=mwlatest.latlonBuilder(mwlatest.dtoken,
                               str(Lat),str(Lon),str(Radius),"",
    "relative_humidity,air_temp,wind_speed,wind_direction,wind_gust,precip_accum_one_hour",
    "","english","english")
    response=mwlatest.readData(url)
    return response
    

def addHyperLinks(weatherStation):
    ID = weatherStation.stid
    Name = weatherStation.name
    #Use NOAA
    baseUrl='https://www.wrh.noaa.gov/mesowest/getobext.php?sid='+ID
#if we want to use the mesonet 
#    baseUrl='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=%s&unit=0&time=LOCAL&product=&year1=&month1=&day1=00&hour1=00&hours=24&graph=1&past=0&order=1' % ID 
    
    htmlSyntax='<a href=\"'+baseUrl+' target="_blank"s"\>'+Name+'</a>'
    return htmlSyntax


def convertTimeZone(timeInt):
    """
    converts Number from Shiny App to Time Zone STring
    """
    validTimes=[1,2,3,4,5,6,7]
    validStringTimes=['America/Los_Angeles','America/Denver','US/Arizona','America/Chicago','America/New_York','Pacific/Honolulu','America/Anchorage']
    timeString=''  
    for i in range(len(validTimes)):
        if timeInt==validTimes[i]:
            timeString=validStringTimes[i]
    return timeString

def runLocator(Lat,Lon,radius,tzID):
    timeZone = ['']
    timeZone[0]=convertTimeZone(float(tzID))
    Location=[Lat,Lon]
    
    weatherData = getRAWSData(Location[0],Location[1],radius)
    wxStations = RAWS.checkStationData(weatherData,timeZone[0],Location)
    
    for i in range(len(wxStations)):
        wxStations[i].name=wxStations[i].name.replace(',','')
        wxStations[i].name=addHyperLinks(wxStations[i])
    
    if len(wxStations)>-1:
        with open(tFile,'w') as f:
            f.write('Name,ID,Temp (F),Wind Spd (mph),Wind Gust(mph),Wind Dir,\
                    Relative Humidity (%),Precip (in),Distance (mi),\
                    Heading,Date,Time,Lat,Lon\n')
            for i in range(len(wxStations)):
                sub = wxStations[i]
                fStr = str(sub.name)+','+\
                str(sub.stid)+','+\
                str(sub.temperature)+','+\
                str(round(sub.windSpeed,1))+','+\
                str(round(sub.windGust,1))+','+\
                str(round(sub.windDirection,1))+','+\
                str(round(sub.rh,1))+','+\
                str(round(sub.precip,1))+','+\
                str(round(sub.distance_from_point,1))+','+\
                str(sub.cardinal)+','+\
                str(sub.date)+','+\
                str(sub.time)+','+\
                str(sub.lat)+','+\
                str(sub.lon)+'\n'
                f.write(fStr)
            f.close()
    else:
        with open(tFile,'wb') as f:
            f.write('Name,ID,Temp (F),Wind Spd (mph),Wind Gust(mph),Wind Dir,\
                    Relative Humidity (%),Precip (in),Distance (mi),\
                    Heading,Date,Time,Lat,Lon\n')
        fStr='NAME,0,0,0,0,0,0,0,0,0,0,0,0\n'
        f.write(fStr)
        f.close()    
    
    print(tFile)

    

def debugMode():
    arg_lat = 47
    arg_lon = -114
    arg_radius = 30
    arg_tzID = 1
    runLocator(arg_lat,arg_lon,arg_radius,arg_tzID)
    
def cliMode():
    arg_lat=float(sys.argv[1])
    arg_lon=float(sys.argv[2])
    arg_radius=float(sys.argv[3])
    arg_tzId=float(sys.argv[4])
    
    runLocator(arg_lat,arg_lon,arg_radius,arg_tzId)
        
    
#debugMode()
cliMode()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    






    
    