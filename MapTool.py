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

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.CMFBTreeFolder import CMFBTreeFolder

from georss import modelGeoRSS

class MapTool(UniqueObject, CMFBTreeFolder):

    """Map Tool
    """

    id = 'portal_maps'
    title = "CPS Map Tool"

    meta_type = 'CPS Map Tool'

    security = ClassSecurityInfo()

    def __init__(self):
        CMFBTreeFolder.__init__(self, self.id)

    security.declareProtected(ManagePortal, 'addMap')
    def addMap(self, id, url):
        """Add a map
        """
        # XXX Why don't you use auto-generated uids ?
        # You may still use a name beside.
        if id in list(self.keys()):
            raise KeyError("A map exists with id: %s" % (id))

        # XXX why don't you store Map objects instead ?
        return self._setOb(id, url)

    # XXX permission ?
    def getMap(self, id):
        """Get a map given its id
        """
        return self._getOb(id)

    # XXX permission ? 
    def getDocumentsByLocation(self, meta_types=[], bounds=[]):
        """Return documents of certain types within specified WGS84 bounds
        """

        catalog = getToolByName(self, 'portal_catalog')

        # XXX Is this an index ?
        brains = catalog(geolocation={'query': 1, 'range': 'min'})
        results = []

        # XXX can't you just use the brains directly ?
        for brain in brains:
            results.append({'id': brain.id, 'title': brain.Title,
                            'description': brain.Description,
                            'type': brain.Type,
                            'date': brain.ModificationDate,
                            'url': brain.getURL(),
                            'poslist': brain.PosList})
        return results

    # XXX permission ? 
    def getGeoRSSModel(self, REQUEST=None):
        """Return a GeoRSS model for mapbuilder
        """
        schemas = self.getDocumentsByLocation()
        if REQUEST:
            REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
        return modelGeoRSS(self.title, self.absolute_url(), schemas)

InitializeClass(MapTool)
