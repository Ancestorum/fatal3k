# -*- coding: utf-8 -*-

#  fatal plugin
#  weather plugin

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploru.net>
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

from fatalapi import *
import pymetar

def get_weather_info(query):
    ccode = query.upper()

    sql = "SELECT desc FROM weather WHERE ccode=?;"
    qres = sqlquery('static/weather.db', sql, ccode)
    
    if not qres:
        sql = "SELECT ccode FROM weather WHERE desc LIKE '?%%';"
        qres = sqlquery('static/weather.db', sql, query)
    
    if qres:
        info = qres[0][0]
        
        return info.replace('&quot;', '"')
    else:
        return ''

def handler_weather(type, source, parameters):
    if parameters:	
        try:
            rf = pymetar.ReportFetcher(parameters.strip())
            fr = rf.FetchReport()
        except Exception as ex:
            return reply(type, source, l('Unknown city code!'))

        rp = pymetar.ReportParser()
        pr = rp.ParseReport(fr)
        tm = time.strptime(pr.getISOTime(), '%Y-%m-%d %H:%M:%SZ')
        tm = time.strftime('%H:%M:%S', tm)
        
        gweather = pr.getWeather()
        gpressure = pr.getPressure()
        
        if gweather:
            gweather = gweather[0].upper() + gweather[1:]
            gweather = l('%s. Temperature:') % (gweather)
        else:
            gweather = 'Temperature:'
            
        if gpressure:
            gpressure = round(gpressure * 0.75, 1)
        
        ccode = parameters.strip()
        
        rep = l('Weather for %s (%s) at %s:\n\n%s') % (pr.getStationName(), ccode.upper(), tm, gweather)
        
        rep += ' %s°C/%s°F. Humidity: %s%%. ' % (pr.getTemperatureCelsius(), pr.getTemperatureFahrenheit(), pr.getHumidity())
        
        if pr.getWindSpeed():
            gwindcomp = pr.getWindCompass()
            gwindir = pr.getWindDirection()
            
            if gwindir and gwindcomp:
                gwindir = '(%s°) at' % (gwindir)
            elif gwindir and not gwindcomp:
                gwindir = '%s° at' % (gwindir)
            else:
                gwindir = ''
            
            if gwindcomp:
                gwindcomp = 'from the %s' % (gwindcomp)
            else:
                gwindcomp = ''
                
            rep += 'Wind: %s %s %s m/s. ' % (gwindcomp, gwindir, int(round(pr.getWindSpeed())))
        if pr.getPressure():
            rep += 'Pressure: %s mmHg (%s hPa). ' % (gpressure, int(round(pr.getPressure())))
        if pr.getSkyConditions():
            rep += 'Sky conditions: %s. ' % (pr.getSkyConditions())
        if pr.getVisibilityKilometers():
            rep += 'Visibility: %s km. ' % (int(round(pr.getVisibilityKilometers())))
        
        return reply(type, source, rep.strip())
    else:
        return reply(type, source, l('Invalid syntax!'))

def handler_weather_code(type, source, parameters):
    if parameters:
        results = get_weather_info(parameters.strip())
        
        if results:
            return reply(type, source, results)
        else:
            return reply(type, source, l('Not found!'))
    else:
        return reply(type, source, l('Invalid syntax!'))
        
register_command_handler(handler_weather, 'weather', 11)
register_command_handler(handler_weather_code, 'ccode', 11)
