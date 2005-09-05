
from Products.CPSInstaller.CPSInstaller import CPSInstaller

class CPSGeoInstaller(CPSInstaller):
        
    product_name = 'CPSGeo'

    def install(self):
        self.log("Starting CPSGeo install")
        self.setupMapTool()
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

