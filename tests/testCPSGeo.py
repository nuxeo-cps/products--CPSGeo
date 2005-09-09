
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
#from Testing import ZopeTestCase
import CPSGeoTestCase

from Products.CPSGeo.Extensions.install import install as install_cpsgeo


class MapTest(CPSGeoTestCase.CPSGeoTestCase):

    def afterSetUp(self):
        self.login('manager')
        install_cpsgeo(self.portal)        

    def beforeTearDown(self):
        self.logout()

    def testMapTool(self):
        print "testMapTools"
        mt = self.portal.portal_maps
        self.assertEquals(mt.meta_type, "CPS Map Tool")
        
       
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapTest))
    return suite
