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
# $Id$

import os
import unittest

from Products.CPSGeo.Map import Map
from Products.CPSGeo.ogclib import wmc

class WMCBaseTestCase(unittest.TestCase):

    def test_contex_bounds(self):
        map_context = self._makeOneContext()
        ebounds = map_context._getBoundingBoxElement()
        self.assertEqual(ebounds.get('minx'), '-180.0')
        self.assertEqual(ebounds.get('miny'), '-90.0')
        self.assertEqual(ebounds.get('maxx'), '180.0')
        self.assertEqual(ebounds.get('maxy'), '90.0')

    def test_contex_bounds_with_initial_value(self):
        map_context = self._makeOneContext(bounds='0 0 0 0')
        ebounds = map_context._getBoundingBoxElement()
        self.assertEqual(ebounds.get('minx'), '0')
        self.assertEqual(ebounds.get('miny'), '0')
        self.assertEqual(ebounds.get('maxx'), '0')
        self.assertEqual(ebounds.get('maxy'), '0')

    def test_contex_bounds_with_incorrect_initial_value(self):
        map_context = self._makeOneContext(bounds='0 0 0')
        self.assertRaises(wmc.WMCError, map_context._getBoundingBoxElement)

    def test_contex_srs(self):
        map_context = self._makeOneContext()
        ebounds = map_context._getBoundingBoxElement()
        self.assertEqual(ebounds.get('SRS'), 'EPSG:4326')

    def test_contex_srs_with_initial_value(self):
        map_context = self._makeOneContext(SRS='EPSG:XXXX')
        ebounds = map_context._getBoundingBoxElement()
        self.assertEqual(ebounds.get('SRS'), 'EPSG:XXXX')

    def test_contex_srs_with_initial_incorrect_value(self):
        map_context = self._makeOneContext(SRS='XXXX')
        self.assertRaises(wmc.WMCError, map_context._getBoundingBoxElement)

    def test_contex_size(self):
        map_context = self._makeOneContext()
        ebounds = map_context._getWindowElement()
        self.assertEqual(ebounds.get('width'), '480')
        self.assertEqual(ebounds.get('height'), '240')

    def test_contex_size_with_initial_value(self):
        map_context = self._makeOneContext(size='800 600')
        ebounds = map_context._getWindowElement()
        self.assertEqual(ebounds.get('width'), '800')
        self.assertEqual(ebounds.get('height'), '600')

    def test_contex_size_with_initial_incorrect_value(self):
        map_context = self._makeOneContext(size='800')
        self.assertRaises(wmc.WMCError, map_context._getWindowElement)

class MapContextTestCase(WMCBaseTestCase):

    def setUp(self):
        self._this_directory = os.path.split(__file__)[0]
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._map = Map('map', url)

    def _makeOneContext(self, **kw):
        return wmc.MapContext(self._map, **kw)

class AggMapContextTestCase(WMCBaseTestCase):

    def setUp(self):
        self._this_directory = os.path.split(__file__)[0]
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._map = Map('map', url)

    def _makeOneContext(self, **kw):
        return wmc.AggregateMapContext(self._map, **kw)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapContextTestCase))
    suite.addTest(unittest.makeSuite(AggMapContextTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')    

    
