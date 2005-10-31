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
"""Map
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ManagePortal

from context import mapToWebMapContext
from ogclib import wms

class Map(PortalContent):

    """Map

    Defines a set of cartographic layers from an external web map service,
    and the default screen size and spatial bounding box. 
    """

    meta_type = portal_type = 'CPS Cartographic Map'
   
    security = ClassSecurityInfo()
    
    def __init__(self, id, url, name=None, title=None, size=(),
                 bounds=(), srs=None, format=None, layers=[]):
        """Initialize"""
        # fix url
        self.url = url.rstrip('?&')
        cap = self._readCapabilities()
        self.name = cap.servicename() or name
        self.title = cap.servicetitle() or title
        self.layernames = cap.layernames()
        self.layertitles = cap.layertitles()
        self.formatlist = cap.getmapformats()
        self.srslist = cap.layersrs()
        self.size = tuple(size)
        self.bounds = tuple(bounds)
        self.srs = srs
        self.format = format
        self.visible_layers = tuple(layers)

    def _getTitle(self, max_length=0):
        """Return a the title of the map

        It will return a title <= max_length.
        If max_lenght=0 then return the complete title
        """
        if max_length == 0:
            return self.title
        else:
            return ''.join(self.title[:max_length])
       
    def _readCapabilities(self):
        # Make a WMS capabilities request
        reader = wms.WMSCapabilitiesReader('1.1.1')
        return reader.read(self.url)
   
    security.declareProtected(View, 'getCapabilitiesURL')
    def getCapabilitiesUrl(self):
        """Return capabilities URL"""
        reader = wms.WMSCapabilitiesReader('1.1.1')
        return reader.capabilities_url(self.url)
        
    security.declareProtected(View, 'mapContext')
    def mapContext(self, REQUEST=None):
        """Return a 1.0 Web Map Context document for use with mapbuilder"""
        if REQUEST:
            REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
        return '<?xml version="1.0" encoding="utf-8"?>' \
               + mapToWebMapContext(self)

    security.declareProtected(ManagePortal, 'editMap')
    def editMap(self, url='', name='', title='', size=[], bounds=[],
                srs=None, format=None, layers=[]):
        """edit map attributes"""

        # Here, reinit the map by fetching back the map from the server
        if url:
            self.__init__(self.getId(), url=url, name=name)
        # Then set the properties
        if name:
            self.name = str(name)
        if title:
            self.title = str(title)
        if size:
            assert len(size) == 2
            self.size = tuple(map(int, size))
        if bounds:
            assert len(bounds) == 4
            self.bounds = tuple(map(float, bounds))
        if srs:
            self.srs = str(srs)
        if format:
            self.format = str(format)
        if layers:
            self.visible_layers = tuple(layers)

    security.declareProtected(ManagePortal, 'manage_editMap')
    def manage_editMap(self, url='', name='', title='', size=[], bounds=[],
                srs=None, format=None, layers=[], REQUEST=None):
        """web front end to editMap"""
        self.editMap(url=url, name=name, title=title, size=size, bounds=bounds,
                     srs=srs, format=format, layers=layers)
        return self.manage_editMapForm(self, REQUEST, update_menu=1)

    #
    # ZMI
    #

    manage_options = (
        {'label': 'Edit', 'action': 'manage_editMapForm'},
        )

    manage_editMapForm = PageTemplateFile('zmi/map_edit_form.pt', globals(),
                                          __name__='manage_editMapForm')

InitializeClass(Map)

def initialize(context):
    context.registerClass(Map, 
                          constructors = (manage_addMapForm, addMap),
                          icon = 'map_context.png')


