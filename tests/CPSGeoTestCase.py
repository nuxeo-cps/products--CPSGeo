from Testing import ZopeTestCase
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSGeo')

CPSTestCase.setupPortal()

class CPSGeoTestCase(CPSTestCase.CPSTestCase):
    pass


