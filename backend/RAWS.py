# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 14:24:29 2018

@author: tanner
"""

import datetime
import dateutil
import numpy
import dateutil.tz
from geopy.distance import great_circle
import math
import PRECIP


class wxStation():
    """
    A class to store weather station data
    """
    variables = {'relative_humidity_value_1':'rh',
                 'wind_speed_value_1':'windSpeed',
                 'wind_direction_value_1':'windDirection',
                 'air_temp_value_1':'temperature',
                 'wind_gust_value_1':'windGust',
                 'precip_accum_one_hour_value_1':'precip'}
    stid = ''
    name = ''
    lat = 0.0
    lon = 0.0
    distance_from_point = 0.0
    bearing = 0.0
    cardinal = ''
    rh = 0.0
    rh_units = '%'
    windSpeed = 0.0
    windGust = 0.0
    windSpeed_units = 'mph'
    windDirection = 0.0
    temperature = 0.0
    temperature_units = 'F'
    precip = 0.0
    precip_units = 'in'    
    date=''
    time=''
    utc_offset = ''

    valid_station=False    
    
    mnet_id = 0

    def printStation(self):
        """
        Print the data stored in the station obj
        """
        print('STID:',self.stid)
        print('NAME:',self.name)
        print('LAT:',self.lat)
        print('LON:',self.lon)
        print('RH:',self.rh)
        print('WINDSPEED:',self.windSpeed)
        print('WINDDIR:',self.windDirection)
        print('WINDGUST:',self.windGust)
        print('TEMPERATURE:',self.temperature)
        print('PRECIP:',self.precip)
        print('DATE_TIME:',self.date,self.time,self.utc_offset)
        print('BEARING:',self.bearing,self.cardinal)
        print('DISTANCE:',self.distance_from_point,"mi")
    
    def set_SensorValue(self,sensorName,sensorValue):
        """
        set the sensor from json data
        """
        setattr(self,self.variables[sensorName],float(sensorValue))
    
    def validateStation(self):
        """
        Correct for empty/bad data
        """
        if(self.windSpeed == 0.0):
            self.windDirection = numpy.nan
        if(self.temperature == 0.0):
            self.temperature = numpy.nan
        if(self.rh == 0.0):
            self.rh = numpy.nan
            
    def set_DateTime(self,odt):
        """
        Set the Date time based on the UTC object parsed
        """
        local = str(odt[1])
        date_local = local[0:10]
        self.date = date_local[5:7]+"/"+date_local[8:]+"/"+date_local[:4]
        self.time = local[11:19]
        self.utc_offset = local[19:]
    
    def set_StationMetaData(self,subStation):
        """
        set general data for the station
        independent of observation
        """
        self.name = str(subStation['NAME'])
        self.stid = str(subStation['STID'])
        self.mnet_id = int(subStation['MNET_ID'])
        self.lat = float(subStation['LATITUDE'])
        self.lon = float(subStation['LONGITUDE'])
    
    def set_stationBearing(self,user_lat,user_lon):
        """
        
        """
        userLoc = [user_lat,user_lon]
        distAndDir = getDistance(userLoc,self)
        self.distance_from_point = distAndDir[0]
        self.bearing = distAndDir[1]
        self.cardinal = distAndDir[2]
    

def degToCompass(num):
    """
    converts Degrees to cardinal Directions
    """
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
#    print arr[(val % 16)]
    return arr[(val % 16)]


def getBearing(lat1,lon1,lat2,lon2):
    """
    
    """
    lat1=math.radians(lat1)
    lon1=math.radians(lon1)
    lat2=math.radians(lat2)
    lon2=math.radians(lon2)
    dLon = lon2 - lon1;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
    brng = math.atan2(y, x)
    brng=math.degrees(brng)
    if brng < 0:
       brng+= 360
    return brng

def getDistance(location,station):
    """
    
    """
    lat1=location[0]
    lon1=location[1]
    lat2=station.lat
    lon2=station.lon
    distance=great_circle([lat1,lon1],[lat2,lon2]).miles #Miles is harded coded for the moment
    bearing=getBearing(lat1,lon1,lat2,lon2)
    cardinal=degToCompass(bearing)
    return [distance,bearing,cardinal]


def parseObservationTime(observation_time,tz):
    """
    Convert a string to a datetime object
    """
    obsD=observation_time[0:10]
    obsT=observation_time[11:19]
    from_zone=dateutil.tz.gettz('UTC')
    to_zone=dateutil.tz.gettz(tz)
    utc=datetime.datetime.strptime(obsD+' '+obsT,'%Y-%m-%d %H:%M:%S')
    
    convert_utc=utc.replace(tzinfo=from_zone)
    local=convert_utc.astimezone(to_zone)
    
    return [utc,local]


def fetchPrecipData(location,radius,stationList):
    precipData = PRECIP.precip(location[0],location[1],radius)
    if(len(precipData.json_data['STATION'])==len(stationList)):     
        for i in range(len(stationList)):
            if(precipData.json_data['STATION'][i]['STID']==stationList[i].stid):
                stationList[i].precip = precipData.json_data['STATION'][i]['OBSERVATIONS']['total_precip_value_1']
#                print(stationList[i].stid)


def checkStationData(station_json,timeZone,location,radius):
    """
    Convert station data in json format to an object
    """
    stationList = []
    if station_json['SUMMARY']['RESPONSE_MESSAGE']!='OK':
        return stationList
    for i in range(len(station_json['STATION'])):
        sub = station_json['STATION'][i]
        station = wxStation()
        utc=datetime.datetime.utcnow()
        min_utc = utc-datetime.timedelta(hours=1.5)
        
        #set some general data
        station.set_StationMetaData(sub)
        
        stationValidity = 0
        #set the sensor data
        sensors = list(sub['OBSERVATIONS'].keys())
        for j in range(len(sensors)):
            sensorValue = sub['OBSERVATIONS'][sensors[j]]['value']
            sensorTime = sub['OBSERVATIONS'][sensors[j]]['date_time']
            obsTime = parseObservationTime(sensorTime,timeZone)
            #check to make sure the observations are from the last hour+.5 hr
            if(obsTime[0]>min_utc):    
                station.set_SensorValue(sensors[j],sensorValue)
                station.set_DateTime(obsTime)
                stationValidity+=1
                
        #sanity check on the station    
        station.validateStation()
        station.set_stationBearing(location[0],location[1])
        
        if(stationValidity>0):
            station.valid_station = True
            stationList.append(station)
            
    fetchPrecipData(location,radius,stationList)
    return stationList




#Debug code   
#import mwlatest
#def getRAWSData(Lat,Lon,Radius):
#    """
#    used mesonet api from mwlatest to fetch 
#    weather station data
#    """
#    url=mwlatest.latlonBuilder(mwlatest.dtoken,
#                               str(Lat),str(Lon),str(Radius),"",
#    "relative_humidity,air_temp,wind_speed,wind_direction,wind_gust,precip_accum_one_hour",
#    "","english","english")
#    response=mwlatest.readData(url)
#    return response
##
#
#testData = getRAWSData(47,-114,15)
#dd=checkStationData(testData,"America/Denver",[47,-114],15)
###
#for i in range(len(dd)):
#    dd[i].printStation()
#    print("\n")
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    