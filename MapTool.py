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

import os.path

from Globals import InitializeClass
from Globals import MessageDialog
from AccessControl import ClassSecurityInfo

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.CMFCore.CMFBTreeFolder import CMFBTreeFolder
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName

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
        utool = getToolByName(self, 'portal_url')
        return os.path.join(
            utool.getRelativeContentURL(self), 'getGeoRSSModel')

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
        utool = getToolByName(self, 'portal_url')
        # XXX : change the title length restriction on the display
        # later on when the widgets will be common to the standalone
        # and CPS ones
        map_ = getattr(self, mapid)
        map_path_ = os.path.join(
            utool.getRelativeContentURL(self), mapid, 'mapContext')
        return {
            'id': mapid,
            'title': map_._getTitle(max_length=30),
            'path': map_path_
            }

    #
    # ZMI
    #

    manage_options = (
        CMFBTreeFolder.manage_options[0],
        ) + \
        ActionProviderBase.manage_options + \
        ({'label': "Map browser",
          'action': 'manage_mapbrowserView',
          },
         ) + \
         CMFBTreeFolder.manage_options[1:]


    security.declareProtected(ManagePortal, 'manage_addMapForm')
    manage_addMapForm = PageTemplateFile('zmi/map_create_form.pt', globals(),
                                         __name__='manage_addMapForm')

    security.declareProtected(ManagePortal, 'manage_geoLocationView')
    manage_mapbrowserView = PageTemplateFile(
        'skins/cpsgeo_standalone/mapbrowser_view.pt', globals(),
        __name__='manage_mapbrowserView')

    security.declareProtected(ManagePortal, 'manage_addMap')
    def manage_addMap(self, id, url, name='', title='', size=[], bounds=[],
                      srs=None, format=None, layers=[], REQUEST=None):
        """Add a Map to a Map tool"""
        try:
            ob = Map(id, url, name, title, size, bounds, srs, format, layers)
        except:
            if REQUEST is not None:
                return MessageDialog(
                    title='Wrong URL',
                    message='URL does not exist '
                            'or is not a correct wms capabilities url',
                    action='%s/manage_addMapForm' % REQUEST['URL1'])
            return None
        else:
            self._setObject(id, ob)
            if REQUEST is not None:
                ob = self._getOb(id)
                return REQUEST.RESPONSE.redirect(
                    self.absolute_url() + '/%s/manage_editMapForm' % (id))
            else:
                return getattr(self, id)

    def all_meta_types(self):
        return ({'name': 'CPS Cartographic Map',
                 'action': 'manage_addMapForm',
                 'permission': ManagePortal},
                )

InitializeClass(MapTool)

