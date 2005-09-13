
from Products.CPSInstaller.CPSInstaller import CPSInstaller

CPS_SKINS = { 'cpsgeo': 'Products/CPSGeo/skins/cpsgeo',
              'cpsgeo_schemas': 'Products/CPSGeo/skins/cpsgeo_schemas' }

class CPSGeoInstaller(CPSInstaller):
        
    product_name = 'CPSGeo'

    def install(self):
        self.log("Starting CPSGeo install")
        self.setupMapTool()
        self.verifySkins(CPS_SKINS)
        self.resetSkinCache()
        # TODO: widgets
        self.verifySchemas(self.portal.getCPSGeoSchemas())
        self.verifyLayouts(self.portal.getCPSGeoLayouts())
        self.finalize()
        self.log("End of specific CPSGeo install")

    def setupMapTool(self):
        self.log("Checking Map Tool")
        self.verifyTool('portal_maps',
                        'CPSGeo',
                        'CPS Map Tool')

                        
def install(self):
    installer = CPSGeoInstaller(self)
    installer.install()
    return installer.logResult()

# For use during development
def uninstall(self):
    self.portal_skins.manage_delObjects(['cpsgeo', 'cpsgeo_schemas'])
    self.portal_schemas.manage_delObjects(['geolocation'])
    self.manage_delObjects(['portal_maps'])
    return 1

