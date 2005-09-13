
from Products.CPSInstaller.CPSInstaller import CPSInstaller

from Products.CPSGeo.Extensions.mapbuilder_installer import install_lib

CPS_SKINS = {
    'cpsgeo': 'Products/CPSGeo/skins/cpsgeo',
    'cpsgeo_document': 'Products/CPSGeo/skins/cpsgeo_document'
    }

class CPSGeoInstaller(CPSInstaller):
        
    product_name = 'CPSGeo'

    def install(self):
        self.log("Starting CPSGeo install")
        self.setupMapTool()
        self.verifySkins(CPS_SKINS)
        self.resetSkinCache()
        self.verifySchemas(self.portal.getCPSGeoSchemas())
        self.verifyLayouts(self.portal.getCPSGeoLayouts())
        self.setupMapBuilderLibs()
        self.finalize()
        self.log("End of specific CPSGeo install")

    def setupMapTool(self):
        self.log("Checking Map Tool")
        self.verifyTool('portal_maps',
                        'CPSGeo',
                        'CPS Map Tool')

    def setupMapBuilderLibs(self):
        """Install mapbuilder within ZODB
        """
        # XXX : split this within a skins dir 
        if 'mapbuilder' in self.portal.objectIds():
            self.portal.manage_delObjects(['mapbuilder'])
        install_lib(self.portal)

                        
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

