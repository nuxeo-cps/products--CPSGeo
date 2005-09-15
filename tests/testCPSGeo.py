
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
#from Testing import ZopeTestCase
import CPSGeoTestCase

from Products.CPSGeo.Extensions.install import install as install_cpsgeo
from Products.CPSGeo import Map

class MapTest(CPSGeoTestCase.CPSGeoTestCase):

    def afterSetUp(self):
        self.login('manager')
        install_cpsgeo(self.portal)        

    def beforeTearDown(self):
        self.logout()

    def testMapTool(self):
        mt = self.portal.portal_maps
        self.assertEquals(mt.meta_type, 'CPS Map Tool')
       
    def testAddMap(self):
        mt = self.portal.portal_maps
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        mt.manage_addMap('map1', url)
        self.assertEquals(mt.mapContexts(), [{'id': 'map1', 'title': 'JPL World Map Service', 'path': '/portal/portal_maps/map1/mapContext'}])
        map1 = getattr(mt, 'map1')
        self.assertEquals(map1.name, 'OGC:WMS')
        self.assertEquals(map1.title, 'JPL World Map Service')
        map1.srs = 'EPSG:4326'
        map1.format = 'image/jpeg'
        map1.bounds = (-120,25,-80,55)
        map1.size = (400,300)
        map1.visible_layers = ('global_mosaic',)
        xml = mt.map1.mapContext()
        f = open('testAddMap.xml', 'w')
        f.write(xml)
        f.close()
         
       
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapTest))
    return suite
