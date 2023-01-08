# -*- coding: utf-8 -*-

#  fatal plugin
#  google plugin

#  Copyright © 2009-2012 Ancestors Soft

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

import sijs

def google_search(query, shw=1):
    try:
        res = urllib.request.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % urllib.parse.quote(query.encode('utf-8')))
        res_dict = sijs.load(res)
    except urllib.error.HTTPError as e:
        return str(e)

    if res_dict['responseStatus'] == 200 and res_dict['responseData']:
        total = sfr_dic_val(res_dict, shw, 'responseData', 'cursor', 'estimatedResultCount')
        results = res_dict['responseData']['results']
        rep = l('Results of search (total: %s; showed: %s):\n\n') % (total, shw)
        
        if not results:
            return ''
        
        for rsi in results[:shw]:
            if rsi['titleNoFormatting']:
                if rsi['titleNoFormatting'][-1] != '!' or rsi['titleNoFormatting'][-1] != '.' or rsi['titleNoFormatting'][-1] != '?':
                    rsi['titleNoFormatting'] += '.'
                rep += '%d) %s\n' % (results.index(rsi) + 1, rsi['titleNoFormatting'])
            
            if rsi['content']:
                if rsi['content'][-1] != '!' or rsi['content'][-1] != '.' or rsi['content'][-1] != '?':
                    rsi['content'] += '.'
                rep += l('Description: %s\n') % (rsi['content'])
                
            rep += l('Link: %s\n') % (rsi['unescapedUrl'])
                        
            if rsi['cacheUrl']:
                rep += l('Cache: %s\n\n') % (rsi['cacheUrl'])
            else:
                rep += '\n'
    
        return rmv_tgs_esc(rep)
    else:
        return l('Unknown error!')

def handler_google_search(type, source, parameters):
    if parameters:
        results = ''
        
        spltdp = parameters.split()
        
        if len(spltdp) >= 1:
            if spltdp[0] == '+':
                results = google_search(parameters, 4)
            else:
                results = google_search(parameters)
        if results:
            return reply(type, source, results.strip())
        else:
            return reply(type, source, l('Nothing found!'))
    else:
        return reply(type, source, l('Invalid syntax!'))

register_command_handler(handler_google_search, 'google', 10)
