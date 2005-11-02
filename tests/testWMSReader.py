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

import unittest

from Products.CPSGeo.ogclib.wms import WMSCapabilitiesReader

class Reader111TestCase(unittest.TestCase):

    def setUp(self):
        self._version = '1.1.1'
        self._url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._reader = WMSCapabilitiesReader(self._version)
        self._cap = self._reader.read(self._url)

    def test_getroot(self):
        self.assertEqual(self._cap.getroot().tag, 'WMT_MS_Capabilities')

    def test_servicename(self):
        self.assertEqual(self._cap.servicename(), 'OGC:WMS')

    def test_servicetitle(self):
        self.assertEqual(self._cap.servicetitle(), 'JPL World Map Service')

    def test_getmapformats(self):
        self.assertEqual(
            self._cap.getmapformats(),
            ('image/jpeg', 'image/png', 'image/geotiff', 'image/tiff'))

    def test_layersrs(self):
        self.assertEqual(
            self._cap.layersrs(), ('EPSG:4326', 'AUTO:42003'))

    def test_layernames(self):
        self.assertEqual(
            self._cap.layernames(),
            ('global_mosaic', 'global_mosaic_base', 'us_landsat_wgs84',
             'srtm_mag', 'us_overlays', 'us90_overlays', 'daily_terra',
             'daily_aqua', 'BMNG', 'modis', 'huemapped_srtm', 'srtmplus',
             'worldwind_dem', 'us_ned', 'us_elevation', 'us_colordem')
            )
    def test_layertitles(self):
        self.assertEqual(
            self._cap.layertitles(),
             ('WMS Global Mosaic, pan sharpened',
              'WMS Global Mosaic, not pan sharpened',
              'CONUS mosaic of 1990 MRLC dataset',
              'SRTM reflectance magnitude, 30m',
              'Progressive US overlay map, white background',
              'MRLC US mosaic with progressive overlay map',
              'Daily composite of MODIS-TERRA images ',
              'Daily composite of MODIS-AQUA images ',
              'Blue Marble Next Generation, Global MODIS derived image',
              'Blue Marble, Global MODIS derived image',
              'SRTM derived global elevation, 3 arc-second, hue mapped',
              'Global 1km elevation, seamless SRTM land elevation '
              'and ocean depth',
              'SRTM derived global elevation, 3 arc-second',
              'United States elevation, 30m',
              'Digital Elevation Map of the United States, DTED dataset, '
              '3 second resolution, grayscale',
              'Digital Elevation Map of the United States, DTED dataset, '
              '3 second resolution, hue mapped')
            )
        
def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(Reader111TestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')    

    
