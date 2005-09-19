from Testing import ZopeTestCase
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSGeo')

class CPSGeoTestCase(CPSTestCase.CPSTestCase):
    pass

class CPSGeoInstaller(CPSTestCase.CPSInstaller):

    def addPortal(self, id):

        # Install the CPS Portal
        CPSTestCase.CPSInstaller.addPortal(self, id)

        # Install the CPSGeo product
        portal = getattr(self.app, id)
        if 'cps_geo_installer' not in portal.objectIds():
            installer = ExternalMethod(
                'cps_geo_installer',
                '',
                'CPSGeo.install',
                'install')
            portal._setObject('cps_geo_installer',
                              installer)
        portal.cps_geo_installer()

CPSTestCase.setupPortal(PortalInstaller=CPSGeoInstaller)


