#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:39:34 2018

@author: tanner
"""

import calcDist
import urllib2

import getpass
import csv
import numpy
import sys

if getpass.getuser()=='tanner':
    dataDir = '/home/tanner/src/nu-weather/RAWS-Locator/radar/'
else:
    dataDir = '/home/ubuntu/src/nuwx/radar/'


def getClosestStation(lat,lon):
    stationFile = dataDir+'radarStations.csv'
    f = open(stationFile,'r')
    stations = list(csv.reader(f))
    distList = []
    for i in range(len(stations)):
        dist = calcDist.getSpatial([lat,lon],[stations[i][1],stations[i][2]])
        distList.append(dist)
    closestStation = stations[numpy.argmin(distList)][0]
    return closestStation
    
def fetchRadar(lat,lon):
    stid = getClosestStation(float(lat),float(lon))
    baseurl='https://radar.weather.gov/ridge/RadarImg/NCR/'
    sid=stid[1:]
    endGif='_NCR_0.gif'
    endGfw='_NCR_0.gfw'
    gifName=dataDir+sid+endGif
    gfwName=dataDir+sid+endGfw
    URL=baseurl+str(sid)+endGif
    urlG=baseurl+str(sid)+endGfw
    
    gifResponse=urllib2.urlopen(URL)
    gfwResponse=urllib2.urlopen(urlG)
    output=open(gifName,'wb')
    gfwOut=open(gfwName,'wb')
    output.write(gifResponse.read())
    gfwOut.write(gfwResponse.read())
    output.close()
    gfwOut.close()
    return gifName

def debugMode():
    uLat = 47.0
    uLon = -115.0
    
    gifN = fetchRadar(uLat,uLon)
    return gifN
    
def cliMode():
    uLat = sys.argv[1]
    uLon = sys.argv[2]
    
    gifN = fetchRadar(uLat,uLon)
    return gifN
    
print cliMode()
        
    
    
    
    
    
    
    