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

from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.CMFBTreeFolder import CMFBTreeFolder
from Products.CMFCore.ActionProviderBase import ActionProviderBase

from georss import brainsToGeoRSS
from Map import Map

class MapTool(UniqueObject, CMFBTreeFolder, ActionProviderBase):

    """Map Tool
    """

    __implements__ = ActionProviderBase.__implements__

    id = 'portal_maps'
    meta_type = title = "CPS Map Tool"

    security = ClassSecurityInfo()

    def __init__(self):
        CMFBTreeFolder.__init__(self, self.id)

    security.declareProtected(View, 'getGeoRSSModel')
    def getGeoRSSModel(self, bbox=[], REQUEST=None):
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

    security.declareProtected(View, 'mapContexts')
    def mapContexts(self):
        """Return a list of dicts describing map id, title, and BASEPATH2-ish
        path to the map context
        """
        contexts = []
        for id_ in list(self.keys()):
            contexts.append(self.mapContextFor(id_))
        return contexts

    security.declareProtected(View, 'mapContextFor')
    def mapContextFor(self, mapid):
        """Return a dict describing the map id, title, and BASEPATH2-ish
        path to the map context given a map id
        """
        base = urlsplit(self.absolute_url())[2]
        map_ = getattr(self, mapid)
        return {'id': mapid, 'title': map_._getTitle(max_length=30),
                'path': os.path.join(base, mapid, 'mapContext')}

    #
    # ZMI
    #

    manage_options = ActionProviderBase.manage_options + \
                     ({'label': "Geo Location View",
                       'action': 'manage_geoLocationView',
                       },
                      {'label': "Geo Location Edit",
                       'action': 'manage_geoLocationEdit',
                       },
                      ) + \
                      CMFBTreeFolder.manage_options

    security.declareProtected(ManagePortal, 'manage_addMapForm')
    manage_addMapForm = PageTemplateFile('zmi/map_create_form.pt', globals(),
                                         __name__='manage_addMapForm')

    security.declareProtected(ManagePortal, 'manage_geoLocationView')
    manage_geoLocationView = PageTemplateFile(
        'skins/cpsgeo_standalone/geo_location_view.pt', globals(),
        __name__='manage_geoLocationView')

    security.declareProtected(ManagePortal, 'manage_geoLocationEdit')
    manage_geoLocationEdit = PageTemplateFile(
        'skins/cpsgeo_standalone/geo_location_edit.pt', globals(),
        __name__='manage_geoLocationEdit')

    security.declareProtected(ManagePortal, 'manage_addMap')
    def manage_addMap(self, id, url, name='', title='', size=[], bounds=[],
                      srs=None, format=None, layers=[], REQUEST=None):
        """Add a Map to a Map tool"""
        ob = Map(id, url, name, title, size, bounds, srs, format, layers)
        self._setObject(id, ob)
        if REQUEST:
            ob = self._getOb(id)
            REQUEST.RESPONSE.redirect(self.absolute_url() +
                                      '/%s/manage_editMapForm' % (id))
        else:
            return getattr(self, id)

    def all_meta_types(self):
        return ({'name': 'CPS Cartographic Map',
                 'action': 'manage_addMapForm',
                 'permission': ManagePortal},
                )

InitializeClass(MapTool)

