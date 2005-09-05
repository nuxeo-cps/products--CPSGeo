# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
# Author: Sean Gillies (sgillies@frii.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$

"""Map Tool
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import UniqueObject
from OFS.Folder import Folder

from Map import Map
from georss import modelGeoRSS


class MapPoolError(Exception):

    """Errors involving a Tool's pool of maps"""
    
    
class MapTool(UniqueObject, Folder):

    """Map Tool
    """

    meta_type = 'CPS Map Tool'

    security = ClassSecurityInfo()

    def __init__(self):
        """Initialize"""
        self.id = 'portal_maps'
        self._maps = {}

    def addMap(self, id, url):
        """Add a map"""
        if id not in self._maps.keys():
            self._maps[id] = url
        else:
            raise MapPoolError, \
            "A map exists with id: %s" % (id)

    def getDocumentsByLocation(self, meta_types=[], bounds=[]):
        """Return documents of certain types within specified WGS84 bounds"""
        brains = self.portal_catalog(geolocation={'query': 1, 'range': 'min'})
        results = []
        for b in brains:
            results.append({'id': b.id, 'title': b.Title,
                            'description': b.Description,
                            'type': b.Type,
                            'date': b.ModificationDate,
                            'url': b.getURL(),
                            'poslist': b.PosList})
        return results
        
    def getGeoRSSModel(self, REQUEST=None):
        """Return a GeoRSS model for mapbuilder"""
        schemas = self.getDocumentsByLocation()
        if REQUEST:
            REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
        return modelGeoRSS(self.title, self.absolute_url(), schemas)
        
        
InitializeClass(MapTool)
