# -*- coding: ISO-8859-15 -*-
# Copyright (c) 2005 Nuxeo SARL <http://nuxeo.com>
# Author : Julien Anguenot <ja@nuxeo.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# $Id: CPSMapDocument.py 26799 2005-09-13 16:44:28Z janguenot $

from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName

from Products.CPSInstaller.CPSInstaller import CPSInstaller

from Products.CPSGeo.Extensions.mapbuilder_installer import install_lib
from Products.CPSGeo.permissions import ManagePortalMaps

CPS_SKINS = {
    'cpsgeo_images': 'Products/CPSGeo/skins/cpsgeo_images',
    'cpsgeo_installer': 'Products/CPSGeo/skins/cpsgeo_installer',
    'cpsgeo_cpscustom': 'Products/CPSGeo/skins/cpsgeo_cpscustom',
    'cpsgeo_config': 'Products/CPSGeo/skins/cpsgeo_config',
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
        self.verifyNewRolesAndPermissions()
        self.verifyWidgets(self.portal.getCPSGeoWidgets())
        self.verifySchemas(self.portal.getCPSGeoSchemas())
        self.verifyLayouts(self.portal.getCPSGeoLayouts())
        self.verifyVocabularies(self.portal.getCPSGeoVocabularies())
        self.setupFlexibleTypes()
        self.setupMapBuilderLibs()
        self.setupCPSGeoActions()
        self.extendCPSMetadata()
        self.setupTranslations()
        self.setupCatalogSpecifics()
        self.finalize()
        self.log("End of specific CPSGeo install")

    def verifyNewRolesAndPermissions(self):
        """Verify new Roles and permissions
        """

        # Setup the new role 
        self.verifyRoles(['PortalMapsManager'])

        # Adjust the permissions for the role
        self.setupPortalPermissions({
            ManagePortalMaps: ['Manager',
                               'PortalMapsManager',
                                ],
            })

        # Extend the roles vocabulary
        vtool = getToolByName(self.portal, 'portal_vocabularies')
        roles_voc = vtool['global_roles']
        roles_voc.set('PortalMapsManager', 'PortalMapsManager',
                      'label_cpsgeo_roles_PortalMapsManager')
        
    def setupMapTool(self):
        """Map Repository Tool
        """
        self.log("Checking Map Tool")
        self.verifyTool('portal_maps', 'CPSGeo', 'CPS Map Tool')

    def setupMapBuilderLibs(self):
        """Install mapbuilder within ZODB
        """
        # XXX : split this within a skins dir

        # Disable useless subscribers during installation
        self.disableEventSubscriber('portal_trees')
        self.disableEventSubscriber('portal_subscriptions')

        if 'mapbuilder' in self.portal.objectIds():
            self.portal.manage_delObjects(['mapbuilder'])
        install_lib(self.portal)

        # Re-enable subscribers
        self.enableEventSubscriber('portal_trees')
        self.enableEventSubscriber('portal_subscriptions')

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

    def setupCPSGeoActions(self):

        self.verifyActionProvider('portal_maps')

        # Cleaning actions
        actiondelmap = {
            'portal_maps': ('cps_map_server',
                            'cps_geolocation',
                            'cps_manage_maps',
                            )
        }
        self.deleteActions(actiondelmap)

        # category : global
        self.portal['portal_maps'].addAction(
            id='cps_manage_maps',
            name='action_cps_manage_maps',
            action='string:${portal_url}/cpsgeo_manage_maps_form',
            condition="",
            permission=(ManagePortalMaps,),
            category='global',
            visible=1)

        # category : object
        self.portal['portal_maps'].addAction(
            id='cps_geolocation',
            name='action_cps_geolocation',
            action='string:${object_url}/cps_geolocation_form',
            condition="python:object != portal",
            permission=(ModifyPortalContent,),
            category='object',
            visible=1)

        self.log(" Added actions for cps map server")

    def extendCPSMetadata(self):
        """Extend CPS Metadata with geo location
        """

        self.log("Extend portal_schemas.metadata with geolocation fields")

        stool = getToolByName(self.portal, 'portal_schemas')
        geolocation = stool['geolocation']
        metadata = stool['metadata']
        for id_ in geolocation.objectIds():
            if id_ in metadata.objectIds():
                metadata.manage_delObjects([id_])
            ob = geolocation[id_]
            metadata._setObject(id_, ob)

        self.log("Extend portal_layouts.metadata with geolocation fields")
        ltool = getToolByName(self.portal, 'portal_layouts')
        geolocation = ltool['geolocation']
        metadata = ltool['metadata']
        for id_ in geolocation.objectIds():
            if id_ in metadata.objectIds():
                metadata.manage_delObjects([id_])
            ob = geolocation[id_]
            metadata._setObject(id_, ob)

        # XXX
        layoutdef = metadata.getLayoutDefinition()
        for widget in geolocation.objectValues():
            to_add = [{'widget_id': widget.getWidgetId(), 'ncols': 2},]
            if to_add not in layoutdef['rows']:
                layoutdef['rows'].append(to_add)
        metadata.setLayoutDefinition(layoutdef)

    def _setupCatalogIndexes(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        indexes = (
            ('pos_list', 'FieldIndex', None),
            )
        for id, type, extra in indexes:
            if id in catalog.indexes() is not None:
                catalog.delIndex(id)
            catalog.addIndex(id, type, extra)
    
    def _setupCatalogMetadata(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        metadata = (
            'pos_list',
            )
        for id in metadata:
            if not catalog._catalog.schema.has_key(id):
                catalog.addColumn(id, None)

    def setupCatalogSpecifics(self):
        """Setup geolocation indexes and metadata
        """
        self._setupCatalogIndexes()
        self._setupCatalogMetadata()
        
def install(self):
    installer = CPSGeoInstaller(self)
    installer.install()
    return installer.logResult()

# For use during development
def uninstall(self):
    self.portal_skins.manage_delObjects(CPS_SKINS.keys())
    self.portal_schemas.manage_delObjects(['geolocation'])
    self.manage_delObjects(['portal_maps'])
    return 1

