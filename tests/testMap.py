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

from Products.CPSGeo.Map import Map

class MapTest(unittest.TestCase):

    def setUp(self):
        self._this_directory = os.path.split(__file__)[0]
        self._url = 'http://wms.jpl.nasa.gov/wms.cgi'

    def test__getTitle(self):
        map_ = Map(id='map', url=self._url)
        # This is the one returned by the wms server.
        self.assertEqual(map_._getTitle(), 'JPL World Map Service')
        # Restricting the length of the title
        self.assertEqual(map_._getTitle(max_length=3), 'JPL')

    def test_editMap(self):
        map_ = Map(id='map', url=self._url)
        map_.editMap(title='The title')
        # Test the new one we explictly specified
        self.assertEqual(map_._getTitle(), 'The title')
        self.assertEqual(map_._getTitle(max_length=3), 'The')

    def test_bounds(self):
        map_ = Map(id='map', url=self._url)
        self.assertEqual((-180.0, -90.0, 180.0, 90.0), map_.bounds)

    def test_map_context(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.mapContext()
        # XXX

    def test_agg_map_context(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.aggMapContext()
        # XXX

    def test_map_context_with_bounds(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.mapContext(kws={'bounds':'0 0 0 0'})
        self.assert_(wmc.find("minx='0'"))
        self.assert_(wmc.find("miny='0'"))
        self.assert_(wmc.find("maxx='0'"))
        self.assert_(wmc.find("maxy='0'"))

    def test_agg_map_context_with_bounds(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.aggMapContext(kws={'bounds':'0 0 0 0'})
        self.assert_(wmc.find("minx='0'"))
        self.assert_(wmc.find("miny='0'"))
        self.assert_(wmc.find("maxx='0'"))
        self.assert_(wmc.find("maxy='0'"))

    def test_map_context_with_srs(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.mapContext(kws={'srs':'EPSG:NUXEO'})
        self.assert_(wmc.find("SRS='NUXEO'"))

    def test_agg_map_context_with_srs(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.aggMapContext(kws={'srs':'EPSG:NUXEO'})
        self.assert_(wmc.find("SRS='NUXEO'"))

    def test_map_context_with_size(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.mapContext(kws={'size':'800 600'})
        self.assert_(wmc.find('height="800"'))
        self.assert_(wmc.find('width="600"'))

    def test_agg_map_context_with_size(self):
        m = Map('map1', self._url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.aggMapContext(kws={'size':'800 600'})
        self.assert_(wmc.find('height="800"'))
        self.assert_(wmc.find('width="600"'))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapTest))
    return suite

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
