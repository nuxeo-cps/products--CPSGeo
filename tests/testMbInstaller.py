
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest

from Testing import ZopeTestCase
from Products.CPSGeo.Extensions.mapbuilder_installer import install_lib

ZopeTestCase.installProduct('CPSGeo')

class MbInstallerTest(ZopeTestCase.ZopeTestCase):

    def test_install_lib(self):
        install_lib(self.folder)
        self.assert_(len(self.folder.mapbuilder.lib._objects) == 10,
                     self.folder.mapbuilder.lib._objects)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MbInstallerTest))
    return suite

