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

from Products.CPSGeo import etree

from Products.CPSGeo.ogclib.wms import WMSCapabilitiesReader
from Products.CPSGeo.ogclib.wms import WMSCapabilitiesInfoset
from Products.CPSGeo.ogclib.wms import WMSError

class Reader111TestCaseBase(unittest.TestCase):

    def setUp(self):
        self._version = '1.1.1'
        self._reader = WMSCapabilitiesReader(self._version)

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

class Reader111TestCase01(Reader111TestCaseBase):

    def setUp(self):
        Reader111TestCaseBase.setUp(self)
        self._url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._cap = self._reader.read(self._url)

    def test_srs(self):
        srs = self._cap.getSRS()
        expected = 'EPSG:4326'
        self.assertEqual(srs, expected)
        
class Reader111TestCase02(Reader111TestCaseBase):

    def setUp(self):
        Reader111TestCaseBase.setUp(self)
        self._service_url = 'http://wms.jpl.nasa.gov/wms.cgi?service=WMS&version=%s&request=GetCapabilities'
        self._cap = self._reader.read(self._service_url)

class Reader111TestCase03(unittest.TestCase):

    def setUp(self):
        this_directory = os.path.split(__file__)[0]
        filepath = os.path.join(
            this_directory,
            'capabilities.xml')
        f = open(filepath, 'r')
        self._cap = WMSCapabilitiesInfoset(etree.fromstring(f.read()))
    
    def test_layerInfo(self):

        info = self._cap.getLayerInfo()
        self.assertEqual(len(info.keys()), 6)

        titles = info.keys()
        titles.sort()

        expected = ['wms.Desserte_Forrestiere',
                    'wms.scan25_037',
                    'wms.Points_eau',
                    'wms.Massifs_forestiers',
                    'wms.Depfla',
                    'wms.Communes_37']
        expected.sort()
        self.assertEqual(titles, expected)
                                 
        self.assertEqual(len(info.values()), 6)
        styles = [x[0] for x in info.values() if x]
        self.assertEqual(len(styles), 5)

    def test_bounds(self):
        bounds = self._cap.getBounds('epsg:27582')
        expected_bounds = (422379, 2.1939e+06, 530821, 2.30234e+06)
        self.assertEqual(bounds, expected_bounds)

    def test_srs(self):
        srs = self._cap.getSRS()
        expected = 'epsg:27582'
        self.assertEqual(srs, expected)

class Reader111TestCase04(unittest.TestCase):

    # To check that the legend url works ok

    def setUp(self):
        this_directory = os.path.split(__file__)[0]
        filepath = os.path.join(
            this_directory,
            'capa_agri.xml')
        f = open(filepath, 'r')
        self._cap = WMSCapabilitiesInfoset(etree.fromstring(f.read()))
    
    def test_layerInfo(self):

        info = self._cap.getLayerInfo()
        self.assertEqual(len(info.keys()), 6)

        titles = info.keys()
        titles.sort()

        expected = ['Communes_37',
                    'Depfla',
                    # Because of the accents
                    u'Dessertes_Foresti\xe8re',
                    'Massifs_forestiers',
                    'Points_d_eau',
                    'scan25_037']

        expected.sort()
        self.assertEqual(titles, expected)
                                 
        self.assertEqual(len(info.values()), 6)
        styles = [x[0] for x in info.values() if x]
        self.assertEqual(len(styles), 5)

#        for iinfo in info:
#            if iinfo:
#                print etree.tostring(info)

class WMSCapabilitiesReaderFromStringTestCase(Reader111TestCase03):

    def setUp(self):
        reader = WMSCapabilitiesReader()
        this_directory = os.path.split(__file__)[0]
        filepath = os.path.join(
            this_directory,
            'capabilities.xml')
        self._cap = reader.readString(open(filepath, 'r').read())

class WMSCapabilitiesReaderURLTestCase(unittest.TestCase):
    
    def test_basic(self):
        qs = '?service=WMS&request=GetCapabilities&version=1.1.1'
        base_url = 'http://foo/bar'
        reader = WMSCapabilitiesReader()
        service_url = reader.capabilities_url(base_url)
        self.assertEqual(service_url, base_url+qs)

    def test_with_map_as_parameter(self):
        qs = '&service=WMS&request=GetCapabilities&version=1.1.1'
        base_url = 'http://foo/bar?map=id'
        reader = WMSCapabilitiesReader()
        service_url = reader.capabilities_url(base_url)
        self.assertEqual(service_url, base_url+qs)

    def test_with_request(self):
        qs = '&service=WMS&version=1.1.1'
        base_url = 'http://foo/bar?map=id&request=GetCapabilities'
        reader = WMSCapabilitiesReader()
        service_url = reader.capabilities_url(base_url)
        self.assertEqual(service_url, base_url+qs)

    def test_with_version(self):
        qs = '&service=WMS&request=GetCapabilities'
        base_url = 'http://foo/bar?map=id&version=1.1.1'
        reader = WMSCapabilitiesReader()
        service_url = reader.capabilities_url(base_url)
        self.assertEqual(service_url, base_url+qs)

    def test_with_service(self):
        qs = '&request=GetCapabilities&version=1.1.1'
        base_url = 'http://foo/bar?service=WMS'
        reader = WMSCapabilitiesReader()
        service_url = reader.capabilities_url(base_url)
        self.assertEqual(service_url, base_url+qs)

class WMSErrorTestCase(unittest.TestCase):

    def setUp(self):
        self._message = 'WMS Error'

    def test_wmserror(self):
        error = WMSError(self._message)
        xml_ = error.toxml()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Reader111TestCase01))
    suite.addTest(unittest.makeSuite(Reader111TestCase02))
    suite.addTest(unittest.makeSuite(Reader111TestCase03))
    suite.addTest(unittest.makeSuite(Reader111TestCase04))
    suite.addTest(unittest.makeSuite(WMSErrorTestCase))
    suite.addTest(unittest.makeSuite(WMSCapabilitiesReaderFromStringTestCase))
    suite.addTest(unittest.makeSuite(WMSCapabilitiesReaderURLTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')    

    
