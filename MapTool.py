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

"""Map Tool For CPS
"""

from urlparse import urlsplit
import os.path

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.CMFBTreeFolder import CMFBTreeFolder

from georss import brainsToGeoRSS
from context import mapToWebMapContext


class MapTool(UniqueObject, CMFBTreeFolder):

    """Map Tool
    """

    id = 'portal_maps'
    title = "CPS Map Tool"

    meta_type = 'CPS Map Tool'

    security = ClassSecurityInfo()

    def __init__(self):
        CMFBTreeFolder.__init__(self, self.id)

    security.declareProtected(View, 'getDocumentsByLocation')
    def getDocumentsByLocation(self, meta_types=[], bounds=[]):
        """Return documents of certain types within specified WGS84 bounds
        """
        catalog = getToolByName(self, 'portal_catalog')
        return catalog(geolocation={'query': 1, 'range': 'min'})

    security.declareProtected(View, 'getGeoRSSModel')
    def getGeoRSSModel(self, REQUEST=None):
        """Return a GeoRSS model for mapbuilder
        """
        brains = self.getDocumentsByLocation()
        if REQUEST:
            REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
        return brainsToGeoRSS(self.title, self.absolute_url(), brains)

    security.declareProtected(View, 'geoRSSPath')
    def geoRSSPath(self):
        """Return a BASEPATH2-ish path to GeoRSS doc for mapbuilder
        """
        base = urlsplit(self.absolute_url())[2]
        return os.path.join(base, 'getGeoRSSModel')

    security.declareProtected(View, 'getMapContext')
    def getMapContext(self, map_id=None, REQUEST=None):
        """Return a 1.0 Web Map Context for mapbuilder
        """
        map = getattr(self, map_id)
        if REQUEST:
            REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
        return '<?xml version="1.0" encoding="utf-8"?>' \
               + mapToWebMapContext(map)

    security.declareProtected(View, 'mapContextPaths')
    def mapContexts(self):
        """Return a list of dicts describing map id, title, and BASEPATH2-ish
        path to the map context
        """
        base = urlsplit(self.absolute_url())[2]
        return [{'id': mapid, 'title': getattr(self, mapid).title,
                 'path': os.path.join(base, mapid, 'mapContext')} \
                for mapid in self.objectIds()]


InitializeClass(MapTool)

