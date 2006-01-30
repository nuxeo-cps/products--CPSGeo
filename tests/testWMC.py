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
from Products.CPSGeo.ogclib import wms

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

# For the next test case testing the encoding of the capilities
# document.
class FakeMap(Map):
    def __init__(self, id, url='', name=None, title=None, size='',
                 bounds="", srs='', format=None, layers=[]):
        """Initialize"""
        this_directory = os.path.split(__file__)[0]
        filepath = os.path.join(
            this_directory,
            'capa_agri.xml')
        reader = wms.WMSCapabilitiesReader('1.1.1')
        self._cap = reader.readString(open(filepath, 'r').read())
        self.name = self._cap.servicename() or name
        self.title = self._cap.servicetitle() or title
        self.layernames = self._cap.layernames()
        self.layertitles = self._cap.layertitles()
        self.formatlist = self._cap.getmapformats()
        self.srslist = self._cap.layersrs()
        self.size = tuple(size)
        self.srs = self._cap.getSRS()
        self.bounds = self._cap.getBounds(self.srs)
        self.format = format
        self.visible_layers = tuple(layers)
        self.url = "http://foo.bar"

    def _readCapabilities(self):
        return self._cap

class EncodingTestCase(unittest.TestCase):

    # agricms usecase

    def setUp(self):
        fake_map = FakeMap('fake')
        self._wmc = wmc.MapContext(map_=fake_map)
        self._aggwmc = wmc.AggregateMapContext(map_=fake_map)

    def test_getLayerElement(self):
        self._wmc._getLayerListElement()
        self._aggwmc._getLayerListElement()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapContextTestCase))
    suite.addTest(unittest.makeSuite(AggMapContextTestCase))
    suite.addTest(unittest.makeSuite(EncodingTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')    

    
