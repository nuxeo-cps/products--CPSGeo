# -*- coding: ISO-8859-15 -*-
# Copyright (c) 2005 Nuxeo SARL <http://nuxeo.com>
# Author : Julien Anguenot <ja@nuxeo.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# $Id: CPSPortlet.py 26680 2005-09-09 14:22:18Z janguenot $

import os
import sys
import unittest

from OFS.Folder import Folder

from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.URLTool import URLTool

from Products.CPSGeo.MapTool import MapTool
from Products.CPSGeo.Map import Map

class MapToolTestCase(unittest.TestCase):

    # Test the MapTool

    def setUp(self):
        self._root = Folder('cps') # site root
        self._root.portal_maps = MapTool()
        self._root.portal_url = URLTool()
        self._maptool = getattr(self._root, 'portal_maps')

    def test_fixtures(self):
        self.assertEqual(self._maptool.id, 'portal_maps')
        self.assertEqual(self._maptool.all_meta_types(),
                         ({'name': 'CPS Cartographic Map',
                           'action': 'manage_addMapForm',
                           'permission': ManagePortal},
                          ))
        self.assertEqual(0, len(self._maptool))

    def test_addMap(self):

        # Add a map in the map tool.
        id_ = 'earth'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        map_ = self._createMap(id_=id_, url=url)
        self.assertEqual(1, len(self._maptool))

        # Fetch the map and check the default params
        map_ = self._maptool[id_]
        self.assert_(map_)
        self.assertEqual(map_.url, url)

    def test_editMap(self):

        # Add a map in the map tool
        id_ = 'earth'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        map_ = self._createMap(id_=id_, url=url)
        self.assertEqual(1, len(self._maptool))

        # Fetch the map
        map_ = self._maptool[id_]
        self.assertEqual(map_.url, url)

        # Edit the map
        map_.editMap(url=url, title='Earth')
        self.assertEqual(1, len(self._maptool))
        map_ = self._maptool[id_]
        self.assertEqual(map_.url, url)
        self.assertEqual(map_.title, 'Earth')

    def test_mapContextFor(self):

        id_ = 'earth'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        map_ = self._createMap(id_=id_, url=url)

        context = self._maptool.mapContextFor(id_)
        expected = {'path': 'portal_maps/earth/mapContext',
                    'id': 'earth', 'title':
                    'JPL World Map Service'}

        self.assertEqual(expected, context)

        # Change the title
        map_.editMap(title='The title')

        context = self._maptool.mapContextFor(id_)
        expected = {'path': 'portal_maps/earth/mapContext',
                    'id': 'earth', 'title':
                    'The title'}

        self.assertEqual(expected, context)

    def test_mapContexts(self):
        id_ = 'earth'
        id2_ = 'earth2'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        map_ = self._createMap(id_=id_, url=url)
        map2_ = self._createMap(id_=id2_, url=url)

        context1 = self._maptool.mapContextFor(id_)
        expected1 = {'path': 'portal_maps/earth/mapContext',
                    'id': 'earth', 'title':
                    'JPL World Map Service'}

        self.assertEqual(expected1, context1)
        
        context2 = self._maptool.mapContextFor(id2_)
        expected2 = {'path': 'portal_maps/earth2/mapContext',
                    'id': 'earth2', 'title':
                    'JPL World Map Service'}

        self.assertEqual(expected1, context1)

        # Check now that mapContexts returns sth consistent
        contexts = self._maptool.mapContexts()
        for context in contexts:
            if context['id'] == id_:
                self.assertEqual(context1, context)
            else:
                self.assertEqual(context2, context)

    def test_geoRSSPath(self):
        rsspath = self._maptool.geoRSSPath()
        self.assertEqual('portal_maps/getGeoRSSModel', rsspath)
                
    #
    # PRIVATE
    #

    def _createMap(self, id_, url, **kw):
        return self._maptool.manage_addMap(id=id_, url=url)
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapToolTestCase))
    return suite

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
