# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 12:53:58 2018

@author: tanner
"""

import urllib
import json
import datetime


class precip():
    """
    A Class to store 
    precipitation data
    """
    def __init__(self,lat,lon,radius):
        self.fetch_lat = lat
        self.fetch_lon = lon
        self.fetch_radius = radius
        
        self.build_url()
        self.fetch_data()
    
    token = '33e3c8ee12dc499c86de1f2076a9e9d4' 
    baseUrl = 'http://api.mesowest.net/v2/stations/precip?'
    
    fetch_radius = 0.0
    fetch_lat = 0.0
    fetch_lon = 0.0
    networks = "1,2"    
    fetch_back = 180 #minutes (3 Hour)
    
    fetch_url = ''    
    json_data = {}
    
    def build_url(self):
        tokStr = '&token='+self.token
        locStr = "&radius="+str(self.fetch_lat)+","+str(self.fetch_lon)+","+str(self.fetch_radius)
        recStr = "&recent="+str(self.fetch_back)
        netStr = "&network="+self.networks
        uniStr = "&units=precip|in"
        
        fullUrl = self.baseUrl+locStr+recStr+netStr+uniStr+tokStr
        self.fetch_url = fullUrl
    
    def fetch_data(self):
        uR = urllib.request.urlopen(self.fetch_url)
        response = uR.read()
        json_string = response.decode()
        a = json.loads(json_string)
        self.json_data = a

