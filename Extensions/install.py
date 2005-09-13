
from Products.CPSInstaller.CPSInstaller import CPSInstaller

from Products.CPSGeo.Extensions.mapbuilder_installer import install_lib

CPS_SKINS = {
    'cpsgeo_standalone': 'Products/CPSGeo/skins/cpsgeo_standalone',
    'cpsgeo_widgets': 'Products/CPSGeo/skins/cpsgeo_widgets',
    'cpsgeo_document': 'Products/CPSGeo/skins/cpsgeo_document'
    }

SECTIONS_ID = 'sections'
WORKSPACES_ID = 'workspaces'

class CPSGeoInstaller(CPSInstaller):

    product_name = 'CPSGeo'

    def install(self):
        self.log("Starting CPSGeo install")
        self.setupMapTool()
        self.verifySkins(CPS_SKINS)
        self.resetSkinCache()
        self.verifySchemas(self.portal.getCPSGeoSchemas())
        self.verifyLayouts(self.portal.getCPSGeoLayouts())
        self.setupFlexibleTypes()
        self.setupMapBuilderLibs()
        self.finalize()
        self.log("End of specific CPSGeo install")

    def setupMapTool(self):
        """Map Repository Tool
        """
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

    def setupFlexibleTypes(self):
        """Install content types

        Allow the creation within workspace / section
        Setup workflow chains
        """

        # skins
        types = self.portal.getCPSGeoTypes()

        self.verifyFlexibleTypes(types)

        self.allowContentTypes(types, 'Workspace')
        self.allowContentTypes(types, 'Section')

        ws_chain = {}
        se_chain = {}
        for k ,v in types.items():
            ws_chain[k] = v.get('cps_workspace_wf', ('workspace_content_wf',))
            ws_chain[k] = ','.join(ws_chain[k])
            se_chain[k] = v.get('cps_section_wf', ('section_content_wf',))
            se_chain[k] = ','.join(se_chain[k])
        self.verifyLocalWorkflowChains(self.portal[WORKSPACES_ID], ws_chain)
        self.verifyLocalWorkflowChains(self.portal[SECTIONS_ID], se_chain)

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

