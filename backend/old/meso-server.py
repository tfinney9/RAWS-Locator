#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 16:16:50 2018

@author: tanner
"""

import mwlatest
import calcUnits
import RAWS_comparator as comparator
import calcTime
import station
import createAlert
import time
import sys
import getpass

#Location=[45.668,-111.0598]
#Location=[38.5449,-121.7405]
#radius=[50.]
numLimit=[0]
#tzId=2
#timeZone=['']
unitLimits={'temp':'Farenheit','tempABV':'F','spd':'miles_per_hour','spdABV':'mph'}
limits={'temp':0,'spd':0,'dir':0,'rain':0,'rh':100,'gust':0}

tDir=''

if getpass.getuser()=='tanner':
    tDir='/home/tanner/src/nu-weather/RAWS-Locator/shiny/data/'
else:
    tDir='/srv/shiny-server/raws/raws-table/data/'


tFile=tDir+'nu-'+str(int(time.time()))+'.csv'

def getRAWSData(Lat,Lon,Radius,limit,spdUnits,tempUnits):
    """
    Internal RAWS fetcher. Uses Mesowest API
    """
    url=mwlatest.latlonBuilder(mwlatest.dtoken,str(Lat),str(Lon),str(Radius),"",
    "relative_humidity,air_temp,wind_speed,wind_direction,wind_gust,precip_accum_one_hour",
    "",str(spdUnits),str(tempUnits))
    response=mwlatest.readData(url)
    return response

#Comment Out  baseUrl to switch between 
#noaa sites and mesowest site
def addHyperLink(wxSt):
    ID=wxSt.stid
    Name=wxSt.name        

    baseUrl='https://www.wrh.noaa.gov/mesowest/getobext.php?sid='+ID
#    baseUrl='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=%s&unit=0&time=LOCAL&product=&year1=&month1=&day1=00&hour1=00&hours=24&graph=1&past=0&order=1' % ID 
#    print baseUrl
    htmlSyntax='<a href=\"'+baseUrl+' target="_blank"s"\>'+Name+'</a>'
    return htmlSyntax

def runNuWx(Lat,Lon,radius,tzId):
    timeZone=['']
    timeZone[0]=calcTime.convertTimeZone(float(tzId))
    Location=[Lat,Lon]
          
    wxData=getRAWSData(Location[0],
                       Location[1],
                        radius,
                        numLimit[0],
                        "english","english")
                        
    wxStationsA=comparator.checkData(wxData,limits,timeZone[0],unitLimits)
    wxStations=comparator.cleanStations(wxStationsA)
    
    wxLoc=createAlert.getStationDirections(Location,wxStations)
    
    for i in range(len(wxStations)):
            wxStations[i].name=wxStations[i].name.replace(',','')
            wxStations[i].name=addHyperLink(wxStations[i])

    #for s1 in wxStations:
    #    station.printStation(s1)
    #    print '\n'
    
#    with open('test','wb') as ff:
#        ff.write(Lat)
#        ff.write('\n')
#        ff.write(Lon)
    
    #fStr=str(wxStations[i].name)+','+wxStations[i].stid+','+str(wxStations[i].temperature)+\
    #','+str(wxStations[i].wind_speed)+','+str(wxStations[i].wind_direction)+','+str(round(wxStations[i].distance_from_point,1))+\
    #','+wxStations[i].cardinal+','+wxStations[i].date+','+wxStations[i].time+','+str(wxStations[i].lat)+','+str(wxStations[i].lon)
    if len(wxStations)>-1:
        with open(tFile,'wb') as f:
            f.write('Name,ID,Temp (F),Wind Spd (mph),Wind Gust(mph),Wind Dir,Relative Humidity (%),Distance (mi),Heading,Date,Time,Lat,Lon\n')
            for i in range(len(wxStations)):
                fStr=str(wxStations[i].name)+','+wxStations[i].stid+','+str(wxStations[i].temperature)+\
                ','+str(wxStations[i].wind_speed)+','+str(wxStations[i].wind_gust)+','+str(wxStations[i].wind_direction)+','+str(round(wxStations[i].rh,1))+','+str(round(wxStations[i].distance_from_point,1))+\
                ','+wxStations[i].cardinal+','+wxStations[i].date+','+wxStations[i].time+','+str(wxStations[i].lat)+\
                ','+str(wxStations[i].lon)+'\n'
                f.write(fStr)
            f.close()
    else:
        with open(tFile,'wb') as f:
            f.write('Name,ID,Temp (F),Wind Spd (mph),Wind Gust(mph),Wind Dir,Distance (mi),Heading,Time,Date,Lat,Lon\n')
            fStr='NAME,0,0,0,0,0,0,0,0,0,0,0\n'
            f.write(fStr)
            f.close()
            
    print tFile

#            for i in range(len(wxStations)):
#                fStr=str(wxStations[i].name)+','+wxStations[i].stid+','+str(wxStations[i].temperature)+\
#                ','+str(wxStations[i].wind_speed)+','+str(wxStations[i].wind_direction)+','+str(round(wxStations[i].distance_from_point,1))+\
#                ','+wxStations[i].cardinal+','+wxStations[i].date+','+wxStations[i].time+','+str(wxStations[i].lat)+\
#                ','+str(wxStations[i].lon)+'\n'
#                f.write(fStr)
#            f.close()


arg_lat=float(sys.argv[1])
arg_lon=float(sys.argv[2])
arg_radius=float(sys.argv[3])
arg_tzId=float(sys.argv[4])
#arg_spd=str(sys.argv[3])
#arg_tmp=str(sys.argv[4])
#arg_hgt=str(sys.argv[5])

#print arg_lat,arg_lon,arg_radius,arg_tzId
runNuWx(arg_lat,arg_lon,arg_radius,arg_tzId)


