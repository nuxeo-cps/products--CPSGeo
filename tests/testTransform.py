#$Id$

import os
import unittest

from cartography.referencing.srs import SpatialReference
from cartography.referencing.transform.proj4 import ProjTransform

class TransformTestCase(unittest.TestCase):
    
    def test_neutral_4326(self):
        src = SpatialReference(epsg=4326)
        dest = SpatialReference(epsg=4326)
        t = ProjTransform(dest, src)
        res = t.transform([(0, 0)])
        self.assertEqual(res, [(0, 0)])

    def test_neutral_4326_27582_01(self):
        src = SpatialReference(epsg=4326)
        dest = SpatialReference(epsg=27582)
        t = ProjTransform(dest, src)
        res = t.transform([(0, 0)])
        self.assertEqual(res, [(600080.5481800643, -3546527.2049124897)])

    def test_neutral_4326_27582_02(self):
        src = SpatialReference(epsg=4326)
        dest = SpatialReference(epsg=27582)
        t = ProjTransform(dest, src)
        res = t.transform([(-5.7418567432569452, 27.140961112260513)])
        self.assertEqual(tuple(map(round, map(float, res[0]))), (0.0, -0.0))

    def test_neutral_27582_4326_01(self):
        dest = SpatialReference(epsg=4326)
        src = SpatialReference(epsg=27582)
        t = ProjTransform(dest, src)
        res = t.transform([(0, 0)])
        self.assertEqual(res, [(-5.7418567432569452, 27.140961112260513)])

    def test_neutral_27582_4326_02(self):
        dest = SpatialReference(epsg=4326)
        src = SpatialReference(epsg=27582)
        t = ProjTransform(dest, src)
        res = t.transform([(600080.5481800643, -3546527.2049124897)])
        self.assertEqual(tuple(map(round, map(float, res[0]))), (0.0, -0.0))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TransformTestCase))
    return suite

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
