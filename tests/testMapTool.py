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

from Products.CMFCore.permissions import ManagePortal

from Products.CPSGeo.MapTool import MapTool
from Products.CPSGeo.Map import Map

class MapToolTestCase(unittest.TestCase):

    # Test the MapTool

    def setUp(self):
        self._maptool = MapTool()

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
        self._maptool.manage_addMap(id=id_, url=url)
        self.assertEqual(1, len(self._maptool))

        # Fetch the map and check the default params
        map_ = self._maptool[id_]
        self.assert_(map_)
        self.assertEqual(map_.url, url)

    def test_editMap(self):

        # Add a map in the map tool
        id_ = 'earth'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._maptool.manage_addMap(id=id_, url=url)
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

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapToolTestCase))
    return suite

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
