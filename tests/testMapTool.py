
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest

from Products.CPSGeo.MapTool import MapTool
from Products.CPSGeo.Map import Map

       
def test_suite():
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(ConfigToolTest))
    return suite
