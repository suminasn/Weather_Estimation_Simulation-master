

'''
    The program is designed to download weather data and location.
    Copyright (C) <2017>  <Sumina SN>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
'''

from __future__ import division
import datetime
import requests
import json
import os
import pandas
from pandas import DataFrame
import forecastio

os.environ['TZ'] = 'UTC'

##################Download location Info##################

def download_location_info(location_list):
    
    geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    elevation_url = 'https://maps.googleapis.com/maps/api/elevation/json?locations='

    location_info_list = []

    for location in location_list:
        try:
            location_info = {'location': location}

            #location info is obtained using google api.
            rgc = requests.get(geocode_url+location).json()
            if rgc.get('results'):
                for rgc_results in rgc.get('results'):
                    latlong = rgc_results.get('geometry','').get('location','')
                    location_info['lat'] = latlong.get('lat','')
                    location_info['lng'] = latlong.get('lng','')

                    #elevation info is obtained from google by using the location data (Latitude and Longitude) obtained.
                    relev = requests.get(elevation_url + str(location_info['lat']) + ',' + str(location_info['lng'])).json()
                    if relev.get("results"):
                        for relev_results in relev.get("results"):
                            location_info['elev'] = relev_results.get("elevation", '')
                            break
                    break
            
            location_info_list.append(location_info)
        except:
            print ("Exception in downloading location info")
            pass
    print(location_info_list)
    return location_info_list

##################Download Weather data##################

def download_weather_data(location_info_list, start_date, api_key):
    weather_data = {}
    for location_info in location_info_list:
        for date_offset in range(0, 365, 7):
            try:
                #weather info is obtained by using the location data (Latitude and Longitude) obtained, through forecastio api.
                forecast = forecastio.load_forecast(
                    api_key,
                    location_info["lat"],
                    location_info["lng"],
                    time=start_date+datetime.timedelta(date_offset),
                    units="us"
                )
                
                for hour in forecast.hourly().data:
                    weather_data['loc'] = weather_data.get('loc', []) + [location_info['location']]
                    weather_data['lat'] = weather_data.get('lat', []) + [location_info['lat']]
                    weather_data['lng'] = weather_data.get('lng', []) + [location_info['lng']]
                    weather_data['elev'] = weather_data.get('elev', []) + [location_info['elev']]
                    weather_data['cond'] = weather_data.get('cond', []) + [hour.d.get('summary', '')]
                    weather_data['temp'] = weather_data.get('temp', []) + [hour.d.get('temperature', 50)]
                    weather_data['hum'] = weather_data.get('hum', []) + [hour.d.get('humidity', 0.5)]
                    weather_data['pres'] = weather_data.get('pres', []) + [hour.d.get('pressure', 1000)]
                    weather_data['time'] = weather_data.get('time', []) + [hour.d['time']]
            except:
                return weather_data
    return weather_data

##################Main Function##################

def main():
    location_list = None
    print ("Begin")
    with open('data/training_locations.txt') as f:
        location_list = [line.strip() for line in f]
    print (location_list)

    #download location Info
    location_info_list = download_location_info(location_list)
    print ("End")

    #download weather data
    weather_data = download_weather_data(location_info_list, datetime.datetime(2015, 1, 1), '790a053f46cda18de23944de6b44fc91')
    if weather_data is not None:

        #writing data to csv file
        df = pandas.DataFrame(weather_data)
        df.to_csv('data/training_weather_data.csv')
        print ("download complete - data creation done")
        return 1
    else:
        print ("Error in data creation")
    return 0

if __name__ == '__main__':
    ret = main()
    if ret == 1:
        print ("success")
    else:
        print ("Failed")
    
