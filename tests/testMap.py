
import os
import sys
import unittest

sys.path.insert(0, '..')
from Products.CPSGeo.Map import Map

class MapTest(unittest.TestCase):

    url = 'http://wms.jpl.nasa.gov/wms.cgi'

    def testMapContext(self):
        m = Map('map1', self.url, size=[640, 480], bounds=[-120,25,-80,55],
                srs='EPSG:4326', layers=['global_mosaic'])
        wmc = m.mapContext()
        self.assert_(wmc.find('<?xml version="1.0" encoding="utf-8"?><wmc:ViewContext') == 0, wmc)
        f = open('testMapContext.xml', 'w')
        f.write(wmc)
        f.close()
        os.system('rm -f testMapContext.xml')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapTest))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())

