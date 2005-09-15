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

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.CMFBTreeFolder import CMFBTreeFolder

from georss import brainsToGeoRSS
from context import mapToWebMapContext
from Map import Map

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
        brains = self.search(REQUEST.form)
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

    security.declareProtected(View, 'mapContexts')
    def mapContexts(self):
        """Return a list of dicts describing map id, title, and BASEPATH2-ish
        path to the map context
        """
        base = urlsplit(self.absolute_url())[2]
        return [{'id': mapid, 'title': getattr(self, mapid).title,
                 'path': os.path.join(base, mapid, 'mapContext')} \
                for mapid in self.objectIds()]

    security.declareProtected(View, 'locatorMapUrl')
    def getLocatorMap(self, REQUEST=None):
        """Return locator map for use in printing"""
        import Image
        import ImageDraw
        from StringIO import StringIO
        image_in = StringIO(self.geo_locator_image.data)
        im = Image.open(image_in)
        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
        REQUEST.RESPONSE.setHeader('Content-type', 'image/png')
        image_out = StringIO()
        im.save(image_out)
        return image_out.getvalue()

    #
    # ZMI
    #

    security.declareProtected(ManagePortal, 'manage_addMapForm')
    manage_addMapForm = PageTemplateFile('zmi/map_create_form.pt', globals(),
                                         __name__='manage_addMapForm')

    def manage_addMap(self, id, url, name='', title='', size=[], bounds=[],
                      srs=None, format=None, layers=[], REQUEST=None):
        """Add a Map to a Map tool"""
        ob = Map(id, url, name, title, size, bounds, srs, format, layers)
        self._setObject(id, ob)
        if REQUEST:
            ob = self._getOb(id)
            REQUEST.RESPONSE.redirect(self.absolute_url()+'/%s/manage_editMapForm' % (id))

    def all_meta_types(self):
        return ({'name': 'CPS Cartographic Map',
                 'action': 'manage_addMapForm',
                 'permission': ManagePortal},
                )        

InitializeClass(MapTool)

