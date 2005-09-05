
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest

from Testing import ZopeTestCase
from Products.CPSGeo.MapTool import MapTool, MapPoolError
from Products.CPSGeo.Map import Map

class ConfigToolTest(unittest.TestCase):
   
    def setUp(self):
        self.url = 'http://gisdata.usgs.net/servlet/com.esri.wms.Esrimap/world'
        version = '1.1.1'
        bounds = [-120,30,-90,50]
        srs = ['EPSG:4326']
        layers = ['Countries', 'cities']
        formats = ['image/jpeg']
        self.usgsmap = Map(self.url, name='name', title='title',
                           version=version, bounds=bounds, srs=srs,
                           layers=layers, formats=formats)
    
    def testAddMap(self):
        tool = MapTool()
        tool.addMap('usgs', self.usgsmap)
        self.assert_(len(tool._maps) == 1, tool._maps)
        self.assert_(tool._maps['usgs'].url == self.url, tool._maps)

    def testAddMapDupe(self):
        tool = MapTool()
        tool.addMap('usgs', self.usgsmap)
        self.assertRaises(MapPoolError, tool.addMap, 'usgs', Map('u'))

       
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConfigToolTest))
    return suite
