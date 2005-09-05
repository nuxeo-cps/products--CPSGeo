
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils as cmfutils
#from Products.CMFCore.CMFCorePermissions import AddPortalContent

registerDirectory('skins', globals())

import MapTool

tools = (MapTool.MapTool,)

def initialize(registrar):
    cmfutils.ToolInit(
        'CPS Geo Tools',
        tools = tools,
        icon = 'tool.png'
        ).initialize(registrar)

