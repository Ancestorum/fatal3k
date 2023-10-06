# -*- coding: utf-8 -*-

#  fatal plugin
#  gismeteo plugin

#  Copyright © 2009-2023 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

__all__ = []

import xml.dom.minidom as mdom
import tempfile
import urllib3

from fatalapi import *

def get_meteo_info(query):
    city = query.lower()

    sql = "SELECT value FROM weather WHERE city=?;"
    qres = sqlquery('static/gismeteo.db', sql, city)
    
    if not qres:
        sql = "SELECT city FROM weather WHERE value=?;"
        qres = sqlquery('static/gismeteo.db', sql, query)
    
    if qres:
        info = qres[0][0]
        
        return info
    else:
        return ''

def get_gis_weather(ccode):
    try:
        url = 'http://informer.gismeteo.ru/xml/%s_1.xml' % (ccode)
        http = urllib3.PoolManager()    
        header = {'User-Agent': 'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.18'}

        resp = http.request('GET', url, headers=header)
        wxml = resp.data
        return wxml
    except Exception:
        return ''
         
def get_element_attvals(dom, element, idx=0):
    try:
        attvals = {}
        elnode = dom.getElementsByTagName(element.upper())
        attkeys = list(elnode[idx].attributes.keys())

        for att in attkeys:
            attvals[att] = elnode[idx].getAttribute(att)

        return attvals
    except Exception:
        return ''
 
def parse_xml(xml):
    try:
        tmpxml = tempfile.TemporaryFile()
        tmpxml.write(xml)
        tmpxml.seek(0)
        
        dom = mdom.parse(tmpxml)
        tmpxml.close()
        
        dom.normalize()
        
        return dom
    except Exception:
        return ''
        
def handler_weather_gismeteo(type, source, parameters):
    gmweekday = {'1': l('Sunday'), '2': l('Monday'), '3': l('Tuesday'), '4': l('Wednesday'), '5': l('Thursday'), '6': l('Friday'), '7': l('Saturday'), '8': l('Sunday')}
    
    gmmonth = {'01': l('january'), '02': l('february'), '03': l('march'), '04': l('april'), '05': l('may'), '06': l('june'), '07': l('july'), '08': l('august'), '09': l('september'), '10': l('october'), '11': l('november'), '12': l('december')}
    
    gmcloudiness = {'0': l('clear'), '1': l('some cloud'), '2': l('cloudy'), '3': l('overcast')}
    
    gmhour = {'01': l('Night'), '02': l('Night'), '03': l('Night'), '04': l('Night'), '05': l('Night'), '06': l('Night'), '07': l('Morning'), '08': l('Morning'), '09': l('Morning'), '10': l('Morning'), '11': l('Morning'), '12': l('Morning'), '13': l('Afternoon'), '14': l('Afternoon'), '15': l('Afternoon'), '16': l('Afternoon'), '17': l('Afternoon'), '18': l('Afternoon'), '19': l('Evening'), '20': l('Evening'), '21': l('Evening'), '22': l('Evening'), '23': l('Evening'), '24': l('Night')}
    
    gmprecipitation = {'4': l('rain'), '5': l('cloudburst'), '6': l('snow'), '7': l('snow'), '8': l('thunderstorm'), '9': l('n/a'), '10': l('no precipitation')}
    
    gmwinddir = {'0': l('N'), '1': l('NE'), '2': l('E'), '3': l('SE'), '4': l('S'), '5': l('SW'), '6': l('W'), '7': l('NW')}

    if parameters:
        city_code = parameters.lower().strip()
        
        ccode = ''
        
        if city_code.isdigit():
            ccode = city_code
            city_code = get_meteo_info(city_code)
            
            if not city_code:
                return reply(type, source, l('Not found!'))
        else:
            ccode = get_meteo_info(city_code)
        
        if ccode:
            wzxml = get_gis_weather(ccode)
            
            if not wzxml:
                return reply(type, source, l('Unknown error!'))

            dom = parse_xml(wzxml)

            if not dom:
                return reply(type, source, l('Parser error!'))

            if city_code.isdigit():
                town = get_meteo_info(city_code)
                town = town.capitalize()
            else:
                town = city_code.capitalize()
            
            rep = l('Weather %s:\n\n') % (town)
            
            indx = 0
            while indx < 4:
                forecast = get_element_attvals(dom, 'forecast', indx)
                day = forecast['day']
                month = forecast['month']
                year = forecast['year']
                hour = forecast['hour']
                rep += l('%s.%s.%s %s:00:\n') % (day, month, year, hour)            
                            
                temperature = get_element_attvals(dom, 'temperature', indx)
                tempmin = temperature['min']
                tempmax = temperature['max']
                rep += l('Temperature: %s-%s°C.\n') % (tempmin, tempmax)
            
                relwet = get_element_attvals(dom, 'relwet', indx)
                wetmin = relwet['min']
                wetmax = relwet['max']
                rep += l('Humidity: %s-%s%%.\n') % (wetmin, wetmax)
            
                wind = get_element_attvals(dom, 'wind', indx)
                ndir = wind['direction']
                wdir = gmwinddir[ndir]
                windmin = wind['min']
                windmax = wind['max']
                rep += l('Wind: %s, %s-%s m/s.\n') % (wdir, windmin, windmax)
            
                pressure = get_element_attvals(dom, 'pressure', indx)
                pressmin = pressure['min']
                pressmax = pressure['max']
                rep += l('Pressure: %s-%s mmHg.\n') % (pressmin, pressmax)
            
                phenomena = get_element_attvals(dom, 'phenomena', indx)
                ncloud = phenomena['cloudiness']
                cloud = gmcloudiness[ncloud]
                nprecip = phenomena['precipitation']
                precip = gmprecipitation[nprecip]
                if indx != 3:
                    rep += l('Sky: %s, %s.\n\n') % (cloud, precip)
                else:
                    rep += l('Sky: %s, %s.') % (cloud, precip)
                indx += 1
            
            return reply(type, source, rep)
        else:
            return reply(type, source, l('Not found!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
        
register_command_handler(handler_weather_gismeteo, 'gismeteo', 11)
