
import sys
import unittest

sys.path.insert(0, '..')
from Map import Map

class MapTest(unittest.TestCase):

    def testInit(self):
        m = Map('url', name='name', title='title', version='version',
                bounds=[-120,30,-90,50],
                srs=['EPSG:4326'],
                layers=['one', 'two'],
                formats=['image/jpeg'])
        self.assert_(m.url == 'url')
        self.assert_(m.name == 'name')
        self.assert_(m.title == 'title')
        self.assert_(m.version == 'version')
        self.assert_(m.bounds == [-120,30,-90,50])
        self.assert_(m.srs == ['EPSG:4326'])
        self.assert_(m.layers == ['one', 'two'])
        self.assert_(m.formats == ['image/jpeg'])
        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapTest))
    return suite
