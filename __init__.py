# -*- coding: ISO-8859-15 -*-
# Copyright (c) 2005 Nuxeo SARL <http://nuxeo.com>

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
# $Id: CPSPortlet.py 26680 2005-09-09 14:22:18Z janguenot $
"""CPSGeo : GIS support for CPS3

http://www.cps-project.org/sections/projects/cpsgeo_simple_gis_for
"""

import AllowModules

from zLOG import LOG, INFO
logKey = 'CPSGeo'

#
# Check first if elementtree is installed. If not it will use lxml.
# lxml runs well but on latest plateform
# See the DEPENDENCIES.txt file for more info on the revisions
#

try:
    import elementtree.ElementTree as etree
    # Monkey Patch adds to the default well known namespaces
    etree._namespace_map.update({
        "http://www.opengis.net/context":               "wmc",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#":  "rdf",
        "http://purl.org/rss/1.0/":                     "rss",
        "http://purl.org/rss/1.0/modules/taxonomy/":    "taxo",
        "http://purl.org/dc/elements/1.1/":             "dc",
        "http://purl.org/rss/1.0/modules/syndication/": "syn",
        "http://www.w3.org/2003/01/geo/wgs84_pos#":     "geo"})
    LOG(logKey, INFO, "will use elementtree as XML library")
except ImportError, e:
    if 'No module named elementtree' not in str(e):
        raise
    try:
        import lxml.etree as etree
        LOG(logKey, INFO, "will use lxml as XML library")
    except ImportError, e:
        if 'No module named lxml' not in str(e):
            msg_ = "requires either elementtree or lxml"
            LOG(logKey, INFO, msg_)
            raise logKey + msg_

## EOF XML lib checks

from Products.CMFCore import utils
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.DirectoryView import registerFileExtension
from Products.CMFCore.FSFile import FSFile

# Register the .xml and .xslt as possible extension for the FSFile
registerFileExtension('xml', FSFile)
LOG(logKey, INFO, "Registers .xml extension for CMFCore.FSFile")
registerFileExtension('xsl', FSFile)
LOG(logKey, INFO, "Registers .xslt extension for CMFCore.FSFile")

import MapTool
import Map
import CPSMapDocument
import CPSWidgets

tools = (MapTool.MapTool,
         )

contentClasses = (
    CPSMapDocument.CPSMapDocument,
    )

contentConstructors = (
    CPSMapDocument.addCPSMapDocument,
    )

fti = ()

registerDirectory('skins', globals())

def initialize(registrar):

    # Content
    utils.ContentInit(
        'CPS Geo Content Types',
        content_types=contentClasses,
        permission=AddPortalContent,
        extra_constructors=contentConstructors,
        fti=fti).initialize(registrar)

    # Tool
    utils.ToolInit(
        'CPS Geo Tools',
        tools=tools,
        icon='tool.png'
        ).initialize(registrar)

